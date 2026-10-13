"""Unit tests for the hardened AnoMod ingestion script without downloading the live dataset.

Validates all security invariants and network error handlers:
1. Resumable transfer via Range headers.
2. Interrupted transfer recovery across retry attempts.
3. Server ignoring Range requests (HTTP 200 clean restart).
4. Malformed and out-of-bounds Content-Range parsing.
5. Rejection of unknown totals ('*') and end-offset mismatches.
6. Short response body rejection.
7. Content-Length mismatch against Content-Range span.
8. Retry exhaustion on persistent HTTP 429 / 5xx.
9. Pre-promotion checksum verification and destination preservation.
10. Atomic promotion with Windows rollback on failure.
11. Preservation of pre-existing verified archives.
12. Cross-platform Zip-Slip defense (POSIX ../, Windows ..\\, drive letters, UNC, ADS, device names).
13. Decompression bomb and single-member size limit enforcement.
14. Extraction target preservation and manifest status tracking (SKIPPED_EXISTING / OVERWRITTEN).
15. Real disk space validation and dry-run reporting.
16. URL provenance tracking (requested URL vs redirected final URL).
"""
from __future__ import annotations

import io
import os
from pathlib import Path
import tempfile
import urllib.error
import zipfile
import pytest

from research.scripts.ingest_anomod import (
    ChecksumMismatchError,
    InsufficientDiskSpaceError,
    SafeDownloadError,
    ZipSlipSecurityError,
    check_available_disk_space,
    compute_file_hashes,
    download_archive_with_resume,
    is_safe_zip_member,
    parse_content_range,
    safe_extract_zip,
    safe_promote_file,
    verify_archive,
    main as ingest_main,
)


class MockResponse:
    def __init__(self, data: bytes, status: int = 200, headers: dict | None = None, url: str | None = None):
        self.data = io.BytesIO(data)
        self.status = status
        self.code = status
        self.headers = headers or {}
        self.url = url or "http://fake.zenodo/AnoMod.zip"

    def read(self, amt: int = -1) -> bytes:
        return self.data.read(amt)

    def geturl(self) -> str:
        return self.url


def test_parse_content_range_valid():
    start, end, total = parse_content_range("bytes 100-199/1000")
    assert start == 100
    assert end == 199
    assert total == 1000

    start_star, end_star, total_star = parse_content_range("bytes 0-499/*")
    assert start_star == 0
    assert end_star == 499
    assert total_star == -1


def test_parse_content_range_malformed_and_out_of_bounds():
    # Invalid unit
    with pytest.raises(ValueError, match="Malformed Content-Range"):
        parse_content_range("items 0-10/100")

    # Start > end
    with pytest.raises(ValueError, match="start .* exceeds end"):
        parse_content_range("bytes 200-100/1000")

    # End >= total
    with pytest.raises(ValueError, match="end index .* out of bounds"):
        parse_content_range("bytes 0-1000/1000")

    # Start >= total
    with pytest.raises(ValueError, match="end index .* out of bounds"):
        parse_content_range("bytes 1000-1005/1000")

    # Non-numeric
    with pytest.raises(ValueError, match="Malformed Content-Range"):
        parse_content_range("bytes abc-def/ghi")


def test_download_range_resume(tmp_path: Path):
    full_data = b"0123456789ABCDEF"
    expected_size = len(full_data)
    dest_path = tmp_path / "test.zip"
    part_path = tmp_path / "test.zip.part"

    # Pre-write first 8 bytes into .part
    part_path.write_bytes(full_data[:8])

    import hashlib
    full_md5 = hashlib.md5(full_data).hexdigest()

    def mock_opener(req, timeout):
        range_hdr = req.get_header("Range")
        assert range_hdr == "bytes=8-"
        headers = {
            "Content-Range": f"bytes 8-15/{expected_size}",
            "Content-Length": "8",
        }
        return MockResponse(full_data[8:], status=206, headers=headers)

    res, final_url = download_archive_with_resume(
        url="http://fake.zenodo/AnoMod.zip",
        dest_path=dest_path,
        expected_size=expected_size,
        expected_md5=full_md5,
        opener=mock_opener,
    )
    assert res == dest_path
    assert dest_path.read_bytes() == full_data
    assert not part_path.exists()


def test_download_unknown_total_asterisk_rejected(tmp_path: Path):
    full_data = b"0123456789ABCDEF"
    dest_path = tmp_path / "test.zip"
    part_path = tmp_path / "test.zip.part"
    part_path.write_bytes(full_data[:8])

    def mock_opener(req, timeout):
        headers = {"Content-Range": "bytes 8-15/*", "Content-Length": "8"}
        return MockResponse(full_data[8:], status=206, headers=headers)

    with pytest.raises(SafeDownloadError, match="Content-Range total is unknown"):
        download_archive_with_resume(
            url="http://fake.zenodo/AnoMod.zip",
            dest_path=dest_path,
            expected_size=len(full_data),
            max_retries=1,
            opener=mock_opener,
        )


def test_download_wrong_end_offset_rejected(tmp_path: Path):
    full_data = b"0123456789ABCDEF"
    dest_path = tmp_path / "test.zip"
    part_path = tmp_path / "test.zip.part"
    part_path.write_bytes(full_data[:8])

    # End is 12 instead of expected 15
    def mock_opener(req, timeout):
        headers = {"Content-Range": f"bytes 8-12/{len(full_data)}", "Content-Length": "5"}
        return MockResponse(full_data[8:13], status=206, headers=headers)

    with pytest.raises(SafeDownloadError, match="Content-Range end mismatch"):
        download_archive_with_resume(
            url="http://fake.zenodo/AnoMod.zip",
            dest_path=dest_path,
            expected_size=len(full_data),
            max_retries=1,
            opener=mock_opener,
        )


def test_download_short_body_rejected(tmp_path: Path):
    full_data = b"0123456789ABCDEF"
    dest_path = tmp_path / "test.zip"
    part_path = tmp_path / "test.zip.part"
    part_path.write_bytes(full_data[:8])

    # Header says 8 bytes, but stream returns only 4
    def mock_opener(req, timeout):
        headers = {"Content-Range": f"bytes 8-15/{len(full_data)}", "Content-Length": "8"}
        return MockResponse(full_data[8:12], status=206, headers=headers)

    with pytest.raises(SafeDownloadError, match="Short response body received"):
        download_archive_with_resume(
            url="http://fake.zenodo/AnoMod.zip",
            dest_path=dest_path,
            expected_size=len(full_data),
            max_retries=1,
            opener=mock_opener,
        )


def test_download_interrupted_transfer_and_recovery(tmp_path: Path):
    full_data = b"0123456789ABCDEF"
    expected_size = len(full_data)
    dest_path = tmp_path / "test.zip"

    import hashlib
    full_md5 = hashlib.md5(full_data).hexdigest()

    call_count = 0

    def mock_opener(req, timeout):
        nonlocal call_count
        call_count += 1
        range_hdr = req.get_header("Range")
        if call_count == 1:
            # First attempt: sends 8 bytes then disconnects
            assert range_hdr is None
            headers = {"Content-Length": "16"}
            return MockResponse(full_data[:8], status=200, headers=headers)
        else:
            # Second attempt: resumes from byte 8
            assert range_hdr == "bytes=8-"
            headers = {"Content-Range": f"bytes 8-15/{expected_size}", "Content-Length": "8"}
            return MockResponse(full_data[8:], status=206, headers=headers)

    res, final_url = download_archive_with_resume(
        url="http://fake.zenodo/AnoMod.zip",
        dest_path=dest_path,
        expected_size=expected_size,
        expected_md5=full_md5,
        initial_backoff=0.01,
        opener=mock_opener,
    )
    assert res == dest_path
    assert dest_path.read_bytes() == full_data
    assert call_count == 2


def test_download_server_ignores_range(tmp_path: Path):
    full_data = b"HELLO_WORLD_12345"
    expected_size = len(full_data)
    dest_path = tmp_path / "test.zip"
    part_path = tmp_path / "test.zip.part"

    # Pre-write 5 bytes
    part_path.write_bytes(b"HELLO")

    import hashlib
    full_md5 = hashlib.md5(full_data).hexdigest()

    def mock_opener(req, timeout):
        return MockResponse(full_data, status=200, headers={"Content-Length": str(expected_size)})

    res, final_url = download_archive_with_resume(
        url="http://fake.zenodo/AnoMod.zip",
        dest_path=dest_path,
        expected_size=expected_size,
        expected_md5=full_md5,
        opener=mock_opener,
    )
    assert res == dest_path
    assert dest_path.read_bytes() == full_data


def test_download_content_range_mismatch(tmp_path: Path):
    dest_path = tmp_path / "test.zip"
    part_path = tmp_path / "test.zip.part"
    part_path.write_bytes(b"1234")

    def mock_opener(req, timeout):
        headers = {"Content-Range": "bytes 0-19/20", "Content-Length": "20"}
        return MockResponse(b"01234567890123456789", status=206, headers=headers)

    with pytest.raises(SafeDownloadError, match="Content-Range start mismatch"):
        download_archive_with_resume(
            url="http://fake.zenodo/AnoMod.zip",
            dest_path=dest_path,
            expected_size=20,
            expected_md5=None,
            max_retries=1,
            opener=mock_opener,
        )


def test_download_content_length_mismatch(tmp_path: Path):
    dest_path = tmp_path / "test.zip"
    part_path = tmp_path / "test.zip.part"
    part_path.write_bytes(b"1234")

    # Content-Range says 4-19 (16 bytes), but Content-Length says 8
    def mock_opener(req, timeout):
        headers = {"Content-Range": "bytes 4-19/20", "Content-Length": "8"}
        return MockResponse(b"01234567", status=206, headers=headers)

    with pytest.raises(SafeDownloadError, match="Content-Length .* does not match Content-Range span"):
        download_archive_with_resume(
            url="http://fake.zenodo/AnoMod.zip",
            dest_path=dest_path,
            expected_size=20,
            expected_md5=None,
            max_retries=1,
            opener=mock_opener,
        )


def test_download_retry_exhaustion_on_429(tmp_path: Path):
    dest_path = tmp_path / "test.zip"

    def mock_opener(req, timeout):
        raise urllib.error.HTTPError(
            url="http://fake.zenodo",
            code=429,
            msg="Too Many Requests",
            hdrs={"Retry-After": "1"},
            fp=None,
        )

    with pytest.raises(SafeDownloadError, match="failed after 2 attempts"):
        download_archive_with_resume(
            url="http://fake.zenodo/AnoMod.zip",
            dest_path=dest_path,
            expected_size=100,
            expected_md5=None,
            max_retries=2,
            initial_backoff=0.01,
            opener=mock_opener,
        )


def test_preserve_existing_valid_archive(tmp_path: Path):
    dest_path = tmp_path / "valid.zip"
    data = b"EXISTING_ARCHIVE_DATA"
    dest_path.write_bytes(data)

    import hashlib
    valid_md5 = hashlib.md5(data).hexdigest()

    def mock_opener(req, timeout):
        raise AssertionError("Opener should not be called when valid archive exists!")

    res, final_url = download_archive_with_resume(
        url="http://fake.zenodo/AnoMod.zip",
        dest_path=dest_path,
        expected_size=len(data),
        expected_md5=valid_md5,
        opener=mock_opener,
    )
    assert res == dest_path


def test_pre_promotion_checksum_failure_leaves_dest_intact(tmp_path: Path):
    dest_path = tmp_path / "dest.zip"
    dest_path.write_bytes(b"ORIGINAL_SAFE_CONTENT")

    part_data = b"CORRUPTED_DOWNLOADED_DATA"

    def mock_opener(req, timeout):
        return MockResponse(part_data, status=200, headers={"Content-Length": str(len(part_data))})

    with pytest.raises(ChecksumMismatchError, match="MD5 mismatch on downloaded file"):
        download_archive_with_resume(
            url="http://fake.zenodo/AnoMod.zip",
            dest_path=dest_path,
            expected_size=len(part_data),
            expected_md5="00000000000000000000000000000000",
            max_retries=1,
            force=True,
            opener=mock_opener,
        )

    assert dest_path.read_bytes() == b"ORIGINAL_SAFE_CONTENT"


def test_safe_promote_file_backup_and_rollback(tmp_path: Path, monkeypatch):
    dest_path = tmp_path / "archive.zip"
    dest_path.write_bytes(b"EXISTING_VALID_CONTENT")

    staging_path = tmp_path / "archive.zip.part"
    staging_path.write_bytes(b"NEW_CONTENT")

    # Monkeypatch rename of staging_path to fail after .bak is created
    orig_rename = Path.rename

    def failing_rename(self, target):
        if str(self).endswith(".part"):
            raise OSError("Simulated Windows disk I/O lock during promotion")
        return orig_rename(self, target)

    monkeypatch.setattr(Path, "rename", failing_rename)

    with pytest.raises(SafeDownloadError, match="Failed to promote archive"):
        safe_promote_file(staging_path, dest_path)

    # Confirm original archive was restored from backup
    assert dest_path.exists()
    assert dest_path.read_bytes() == b"EXISTING_VALID_CONTENT"


def test_verify_archive_checksum_failure(tmp_path: Path):
    test_file = tmp_path / "archive.zip"
    test_file.write_bytes(b"some data")

    with pytest.raises(ChecksumMismatchError, match="Archive size mismatch"):
        verify_archive(test_file, expected_size=999)

    with pytest.raises(ChecksumMismatchError, match="MD5 mismatch"):
        verify_archive(test_file, expected_size=len(b"some data"), expected_md5="00000000000000000000000000000000")


def test_safe_extract_zip_success_and_skipping(tmp_path: Path):
    archive_path = tmp_path / "valid.zip"
    extract_dir = tmp_path / "extracted"

    with zipfile.ZipFile(archive_path, "w") as zf:
        zf.writestr("folder/file1.txt", "content 1")
        zf.writestr("folder/sub/file2.txt", "content 2")

    manifest = safe_extract_zip(archive_path, extract_dir)
    assert len(manifest) == 2
    assert manifest[0]["status"] == "EXTRACTED"
    assert (extract_dir / "folder" / "file1.txt").read_text() == "content 1"

    (extract_dir / "folder" / "file1.txt").write_text("modified content")

    manifest2 = safe_extract_zip(archive_path, extract_dir, overwrite=False)
    assert manifest2[0]["status"] == "SKIPPED_EXISTING"
    assert (extract_dir / "folder" / "file1.txt").read_text() == "modified content"

    manifest3 = safe_extract_zip(archive_path, extract_dir, overwrite=True)
    assert manifest3[0]["status"] == "OVERWRITTEN"
    assert (extract_dir / "folder" / "file1.txt").read_text() == "content 1"


def test_safe_extract_zip_decompression_bomb_rejected(tmp_path: Path):
    archive_path = tmp_path / "big.zip"
    extract_dir = tmp_path / "extracted"

    with zipfile.ZipFile(archive_path, "w") as zf:
        zf.writestr("file1.txt", b"A" * 500)
        zf.writestr("file2.txt", b"B" * 600)

    # Set max total bytes to 1000 (total uncompressed is 1100)
    with pytest.raises(SafeDownloadError, match="Total uncompressed archive size .* exceeds safety threshold"):
        safe_extract_zip(archive_path, extract_dir, max_total_bytes=1000)


def test_safe_extract_zip_oversized_member_rejected(tmp_path: Path):
    archive_path = tmp_path / "big_member.zip"
    extract_dir = tmp_path / "extracted"

    with zipfile.ZipFile(archive_path, "w") as zf:
        zf.writestr("file1.txt", b"A" * 800)

    # Set max single member bytes to 500
    with pytest.raises(SafeDownloadError, match="uncompressed size .* exceeds maximum allowed limit"):
        safe_extract_zip(archive_path, extract_dir, max_member_bytes=500)


def test_safe_extract_zip_slip_and_cross_platform_attacks(tmp_path: Path):
    extract_dir = tmp_path / "extracted"

    assert not is_safe_zip_member("../evil.txt", extract_dir)
    assert not is_safe_zip_member("..\\evil.txt", extract_dir)
    assert not is_safe_zip_member("/evil.txt", extract_dir)
    assert not is_safe_zip_member("C:evil.bat", extract_dir)
    assert not is_safe_zip_member("C:/evil.bat", extract_dir)
    assert not is_safe_zip_member("\\\\server\\share\\evil.txt", extract_dir)
    assert not is_safe_zip_member("data:stream", extract_dir)
    assert not is_safe_zip_member("CON.txt", extract_dir)
    assert not is_safe_zip_member("NUL", extract_dir)
    assert not is_safe_zip_member("folder/../../evil.txt", extract_dir)
    assert is_safe_zip_member("folder/sub/valid.csv", extract_dir)

    archive_path = tmp_path / "malicious.zip"
    with zipfile.ZipFile(archive_path, "w") as zf:
        zf.writestr("../evil.txt", "pwned")

    with pytest.raises(ZipSlipSecurityError, match="Zip-slip attempt rejected"):
        safe_extract_zip(archive_path, extract_dir)


def test_provenance_records_requested_and_final_url(tmp_path: Path):
    test_file = tmp_path / "archive.zip"
    test_file.write_bytes(b"PROVENANCE_TEST_DATA")

    import hashlib
    h_md5 = hashlib.md5(b"PROVENANCE_TEST_DATA").hexdigest()

    prov = verify_archive(
        archive_path=test_file,
        expected_size=len(b"PROVENANCE_TEST_DATA"),
        expected_md5=h_md5,
        requested_url="http://fake.zenodo/AnoMod.zip",
        final_url="https://zenodo.org/records/18342898/files/AnoMod.zip?download=1",
    )
    assert prov.requested_url == "http://fake.zenodo/AnoMod.zip"
    assert prov.final_url == "https://zenodo.org/records/18342898/files/AnoMod.zip?download=1"
    assert prov.source_checksum_verified is True
    assert prov.file_size_bytes == len(b"PROVENANCE_TEST_DATA")


def test_check_disk_space():
    is_ok, free_gb, req_gb = check_available_disk_space(Path("."), 1024)
    assert is_ok is True
    assert free_gb > 0


def test_ingest_main_dry_run():
    exit_code = ingest_main(["--dry-run"])
    assert exit_code == 0
