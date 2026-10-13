"""AegisOps — Safe, Resumable AnoMod Benchmark Ingestion Script.

Provides a robust, interruptible, and verifiable transfer client for the
external AnoMod benchmark dataset (Zenodo DOI: 10.5281/zenodo.18342898).

Enforces:
1. Resumable chunked transfer via HTTP Range headers.
2. Strict Content-Range (start/end/total) and response-length validation.
3. Rejection of unknown totals ('*') and inconsistent totals for known-size archives.
4. Correct handling of servers that ignore Range requests (restarts cleanly from 0).
5. Bounded retries with exponential backoff and jitter for HTTP 429, 5xx, and drops.
6. Safe pre-promotion verification and atomic promotion with Windows rollback backup.
7. Cryptographic provenance tracking (source MD5 verification vs local SHA-256 integrity).
8. Cross-platform Zip-Slip defense (POSIX + Windows drive/UNC/device/stream containment).
9. Decompression bomb limits (maximum total uncompressed size and single-member limit).
10. Safe extraction target handling with file skipping and manifest tracking.
11. Real disk space verification using shutil.disk_usage.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import hashlib
import json
import logging
import os
from pathlib import Path
import random
import re
import shutil
import sys
import time
from typing import Any, Callable, Dict, List, Optional, Tuple
import urllib.error
import urllib.parse
import urllib.request
import zipfile

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger("ingest_anomod")

# Authoritative dataset metadata
DEFAULT_ZENODO_RECORD_URL = "https://zenodo.org/records/18342898"
DEFAULT_ARCHIVE_URL = "https://zenodo.org/records/18342898/files/AnoMod.zip?download=1"
EXPECTED_ARCHIVE_NAME = "AnoMod.zip"
EXPECTED_SIZE_BYTES = 201_917_396  # 201.9 MB (Zenodo exact byte size)
EXPECTED_MD5 = "30c5835190c3550c5efc34d6be4f9238"
DEFAULT_DEST_DIR = Path("data/external/anomod")
DEFAULT_TIMEOUT_SECONDS = 30
DEFAULT_CHUNK_SIZE = 1024 * 1024  # 1 MiB
DEFAULT_MAX_RETRIES = 10
DEFAULT_INITIAL_BACKOFF = 1.0
DEFAULT_MAX_BACKOFF = 60.0

# Conservative storage requirements: 201.9 MB archive + ~1.2 GB extracted + safety margin
DEFAULT_REQUIRED_STORAGE_BYTES = 3 * 1024 * 1024 * 1024  # 3.0 GiB

# Decompression safety limits
DEFAULT_MAX_TOTAL_UNCOMPRESSED_BYTES = 5 * 1024 * 1024 * 1024  # 5 GiB
DEFAULT_MAX_SINGLE_MEMBER_BYTES = 1024 * 1024 * 1024  # 1 GiB

WINDOWS_RESERVED_DEVICE_NAMES = {
    "CON", "PRN", "AUX", "NUL",
    "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
    "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9",
}


@dataclass
class TransferProvenance:
    requested_url: str
    final_url: str
    archive_name: str
    file_size_bytes: int
    expected_size_bytes: int
    md5_hash: str
    expected_md5: Optional[str]
    sha256_hash: str
    download_timestamp_utc: str
    status: str
    source_checksum_verified: bool
    notes: str

    @property
    def url(self) -> str:
        return self.requested_url


class SafeDownloadError(Exception):
    """Base exception for safe download failures."""
    pass


class ChecksumMismatchError(SafeDownloadError):
    """Raised when downloaded file fails size or hash verification."""
    pass


class ZipSlipSecurityError(SafeDownloadError):
    """Raised when an archive member attempts directory traversal."""
    pass


class InsufficientDiskSpaceError(SafeDownloadError):
    """Raised when free disk space is insufficient for transfer or extraction."""
    pass


def compute_file_hashes(file_path: Path) -> tuple[str, str]:
    """Compute MD5 and SHA-256 hashes of a local file in streaming chunks."""
    md5 = hashlib.md5()
    sha256 = hashlib.sha256()
    with file_path.open("rb") as f:
        while chunk := f.read(1024 * 1024):
            md5.update(chunk)
            sha256.update(chunk)
    return md5.hexdigest(), sha256.hexdigest()


def check_available_disk_space(target_dir: Path, required_bytes: int) -> tuple[bool, float, float]:
    """Check available free space on the drive hosting target_dir.
    
    Returns (is_sufficient, free_gb, required_gb).
    """
    target_dir = Path(target_dir).resolve()
    check_dir = target_dir
    while not check_dir.exists() and check_dir.parent != check_dir:
        check_dir = check_dir.parent
    if not check_dir.exists():
        check_dir = Path.cwd()

    usage = shutil.disk_usage(check_dir)
    free_bytes = usage.free
    free_gb = free_bytes / (1024 ** 3)
    required_gb = required_bytes / (1024 ** 3)
    return (free_bytes >= required_bytes, free_gb, required_gb)


def parse_content_range(header_val: str) -> tuple[int, int, int]:
    """Parse and strictly validate 'bytes <start>-<end>/<total>' header string.
    
    Returns (start, end, total).
    Raises ValueError on malformed or invalid range syntax.
    """
    if not header_val or not isinstance(header_val, str):
        raise ValueError("Empty or missing Content-Range header value.")
    
    header_val = header_val.strip()
    match = re.match(r"^bytes\s+(\d+)-(\d+)/(\d+|\*)$", header_val)
    if not match:
        raise ValueError(f"Malformed Content-Range syntax: '{header_val}'. Expected 'bytes <start>-<end>/<total>'.")

    start = int(match.group(1))
    end = int(match.group(2))
    total_str = match.group(3)
    total = int(total_str) if total_str != "*" else -1

    if start > end:
        raise ValueError(f"Invalid Content-Range: start ({start}) exceeds end ({end}).")
    if total != -1:
        if end >= total:
            raise ValueError(f"Invalid Content-Range: end index ({end}) out of bounds for total ({total}).")
        if start >= total:
            raise ValueError(f"Invalid Content-Range: start index ({start}) out of bounds for total ({total}).")

    return start, end, total


def is_safe_zip_member(member_name: str, extract_root: Path) -> bool:
    r"""Validate whether an archive member is safe to extract under extract_root.
    
    Protects against:
    - POSIX directory traversal (../)
    - Windows backslash traversal (..\)
    - Drive absolute paths (C:, D:)
    - UNC network shares (\\server\share, //server/share)
    - NTFS Alternate Data Streams (colon in filename)
    - Windows reserved device names (CON, PRN, AUX, NUL, COM1-9, LPT1-9)
    - Escapes from extract_root after path resolution
    """
    if not member_name or not isinstance(member_name, str):
        return False

    clean = member_name.replace("\\", "/")

    # Reject leading slashes or UNC paths
    if clean.startswith("/") or clean.startswith("//"):
        return False

    # Reject Windows drive letters (e.g., C:file or C:/file)
    if re.match(r"^[a-zA-Z]:", clean):
        return False

    # Reject NTFS Alternate Data Streams
    if ":" in clean:
        return False

    # Check for traversal components
    parts = clean.split("/")
    for part in parts:
        if part in ("..", "."):
            return False
        # Check Windows reserved device names
        stem = part.split(".")[0].upper()
        if stem in WINDOWS_RESERVED_DEVICE_NAMES:
            return False

    # Resolve target and confirm it is strictly within extract_root
    extract_root = extract_root.resolve()
    target_path = (extract_root / clean).resolve()
    try:
        target_path.relative_to(extract_root)
    except ValueError:
        return False

    return True


def safe_promote_file(staging_path: Path, dest_path: Path) -> None:
    """Atomically promote staging_path to dest_path with Windows-safe backup and rollback.
    
    If dest_path already exists, it is renamed to .bak before promotion.
    If promotion fails, the backup is restored to dest_path.
    """
    dest_path = Path(dest_path).resolve()
    staging_path = Path(staging_path).resolve()
    backup_path = dest_path.with_name(dest_path.name + ".bak")

    has_backup = False
    if dest_path.exists():
        if backup_path.exists():
            backup_path.unlink()
        dest_path.rename(backup_path)
        has_backup = True

    try:
        if dest_path.exists():
            dest_path.unlink()
        staging_path.rename(dest_path)
        if has_backup and backup_path.exists():
            backup_path.unlink()
    except Exception as exc:
        logger.error("Promotion failed: %s. Rolling back destination archive.", exc)
        if has_backup and backup_path.exists() and not dest_path.exists():
            backup_path.rename(dest_path)
        raise SafeDownloadError(f"Failed to promote archive to {dest_path}: {exc}") from exc


def download_archive_with_resume(
    url: str,
    dest_path: Path,
    expected_size: int = EXPECTED_SIZE_BYTES,
    expected_md5: Optional[str] = EXPECTED_MD5,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    max_retries: int = DEFAULT_MAX_RETRIES,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
    initial_backoff: float = DEFAULT_INITIAL_BACKOFF,
    max_backoff: float = DEFAULT_MAX_BACKOFF,
    force: bool = False,
    opener: Optional[Callable[[urllib.request.Request, int], Any]] = None,
) -> Tuple[Path, str]:
    """Download an archive with partial resumption, pre-promotion checksum check, and backoff.
    
    Returns (dest_path, final_url).
    
    Invariants:
    1. If dest_path exists, has expected_size, and valid MD5, returns dest_path without re-downloading (unless force=True).
    2. Uses a temporary `.part` file during download.
    3. Promotes `.part` to `dest_path` ONLY AFTER size and checksum verification succeed.
    4. Preserves any existing `dest_path` via rollback if an error occurs.
    """
    dest_path = Path(dest_path).resolve()
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    part_path = dest_path.with_name(dest_path.name + ".part")
    final_url = url

    # Check if dest_path is already present and valid
    if dest_path.exists() and not force:
        if dest_path.stat().st_size == expected_size:
            logger.info("Destination archive %s already exists with expected size. Verifying checksum...", dest_path)
            md5_cur, _ = compute_file_hashes(dest_path)
            if expected_md5 is None or md5_cur.lower() == expected_md5.lower():
                logger.info("Existing destination archive is verified. Skipping re-download.")
                return dest_path, final_url
            else:
                logger.warning("Existing archive checksum mismatch (%s != %s). Re-download required.", md5_cur, expected_md5)
        else:
            logger.warning("Existing archive size mismatch (%d != %d). Re-download required.", dest_path.stat().st_size, expected_size)

    # Check available disk space (require 3.0 GB conservative storage)
    is_ok, free_gb, req_gb = check_available_disk_space(dest_path.parent, DEFAULT_REQUIRED_STORAGE_BYTES)
    if not is_ok:
        raise InsufficientDiskSpaceError(
            f"Insufficient disk space on {dest_path.parent}: {free_gb:.2f} GB free, {req_gb:.2f} GB required."
        )

    retries = 0
    backoff = initial_backoff

    while retries < max_retries:
        current_bytes = part_path.stat().st_size if part_path.exists() else 0

        if current_bytes > expected_size:
            logger.warning(
                "Existing partial file (%d bytes) exceeds expected size (%d). Truncating.",
                current_bytes,
                expected_size,
            )
            part_path.unlink()
            current_bytes = 0

        if current_bytes == expected_size:
            logger.info("Partial file matches expected size (%d bytes). Verifying checksum before promotion.", current_bytes)
            part_md5, _ = compute_file_hashes(part_path)
            if expected_md5 and part_md5.lower() != expected_md5.lower():
                logger.error("Partial file failed MD5 check: expected %s, got %s. Discarding.", expected_md5, part_md5)
                part_path.unlink()
                current_bytes = 0
            else:
                logger.info("Checksum verified on partial file. Promoting to %s.", dest_path)
                safe_promote_file(part_path, dest_path)
                return dest_path, final_url

        req = urllib.request.Request(url, headers={"User-Agent": "AegisOps-Ingest/1.0"})
        is_resuming = current_bytes > 0
        if is_resuming:
            req.add_header("Range", f"bytes={current_bytes}-")
            logger.info("Requesting range bytes=%d- for %s", current_bytes, url)

        try:
            if opener is not None:
                resp = opener(req, timeout)
            else:
                resp = urllib.request.urlopen(req, timeout=timeout)

            status = getattr(resp, "status", getattr(resp, "code", 200))
            if hasattr(resp, "geturl"):
                final_url = resp.geturl()
            elif hasattr(resp, "url"):
                final_url = resp.url

            expected_span = expected_size - current_bytes if is_resuming else expected_size

            if is_resuming:
                if status == 206:
                    cr = resp.headers.get("Content-Range", "")
                    if not cr:
                        raise SafeDownloadError("Server returned 206 Partial Content but omitted Content-Range header.")
                    start, end, total = parse_content_range(cr)
                    if total == -1:
                        raise SafeDownloadError(
                            f"Content-Range total is unknown ('*'), but archive size is known ({expected_size})."
                        )
                    if total != expected_size:
                        raise SafeDownloadError(
                            f"Content-Range total mismatch: expected {expected_size}, received {total}."
                        )
                    if start != current_bytes:
                        raise SafeDownloadError(
                            f"Content-Range start mismatch: expected {current_bytes}, received {start}."
                        )
                    if end != expected_size - 1:
                        raise SafeDownloadError(
                            f"Content-Range end mismatch: expected {expected_size - 1}, received {end}."
                        )
                    expected_span = end - start + 1

                    # Validate response content length against Content-Range span if header present
                    cl_hdr = resp.headers.get("Content-Length")
                    if cl_hdr and cl_hdr.isdigit():
                        if int(cl_hdr) != expected_span:
                            raise SafeDownloadError(
                                f"Content-Length ({cl_hdr}) does not match Content-Range span ({expected_span})."
                            )
                elif status == 200:
                    # Server ignored Range header and sent full stream from byte 0
                    logger.warning("Server ignored Range request (returned HTTP 200); restarting from byte 0.")
                    current_bytes = 0
                    if part_path.exists():
                        part_path.unlink()
                    expected_span = expected_size
                    cl_hdr = resp.headers.get("Content-Length")
                    if cl_hdr and cl_hdr.isdigit() and int(cl_hdr) != expected_size:
                        raise SafeDownloadError(
                            f"Content-Length ({cl_hdr}) does not match expected size ({expected_size})."
                        )
                else:
                    raise SafeDownloadError(f"Unexpected HTTP status {status} on range request.")
            else:
                if status != 200:
                    raise SafeDownloadError(f"Unexpected HTTP status {status} on fresh download request.")
                cl_hdr = resp.headers.get("Content-Length")
                if cl_hdr and cl_hdr.isdigit() and int(cl_hdr) != expected_size:
                    raise SafeDownloadError(
                        f"Content-Length ({cl_hdr}) does not match expected size ({expected_size})."
                    )

            mode = "ab" if (is_resuming and status == 206) else "wb"
            bytes_read_this_resp = 0
            with part_path.open(mode) as out_f:
                while True:
                    chunk = resp.read(chunk_size)
                    if not chunk:
                        break
                    out_f.write(chunk)
                    bytes_read_this_resp += len(chunk)

            if bytes_read_this_resp != expected_span:
                raise SafeDownloadError(
                    f"Short response body received: expected {expected_span} bytes, received {bytes_read_this_resp} bytes."
                )

            # Check downloaded size on partial file
            final_part_size = part_path.stat().st_size
            if final_part_size == expected_size:
                logger.info("Download stream reached expected size (%d bytes). Verifying checksum...", final_part_size)
                part_md5, _ = compute_file_hashes(part_path)
                if expected_md5 and part_md5.lower() != expected_md5.lower():
                    raise ChecksumMismatchError(
                        f"MD5 mismatch on downloaded file: expected {expected_md5}, computed {part_md5}."
                    )
                logger.info("Checksum verified successfully. Promoting to destination archive: %s", dest_path)
                safe_promote_file(part_path, dest_path)
                return dest_path, final_url
            elif final_part_size < expected_size:
                raise SafeDownloadError(
                    f"Download disconnected prematurely: received {final_part_size} / {expected_size} bytes."
                )
            else:
                raise SafeDownloadError(
                    f"Downloaded bytes ({final_part_size}) exceeded expected size ({expected_size})."
                )

        except (ChecksumMismatchError, InsufficientDiskSpaceError):
            # Permanent errors: abort immediately without retry
            raise
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError, ConnectionError, SafeDownloadError) as exc:
            retries += 1
            retry_after = None
            if isinstance(exc, urllib.error.HTTPError):
                if exc.code == 429:
                    retry_after_hdr = exc.headers.get("Retry-After")
                    if retry_after_hdr and retry_after_hdr.isdigit():
                        retry_after = float(retry_after_hdr)
                logger.warning("HTTP Error %s on attempt %d/%d: %s", exc.code, retries, max_retries, exc)
            else:
                logger.warning("Transfer error on attempt %d/%d: %s", retries, max_retries, exc)

            if retries >= max_retries:
                logger.error("Exhausted all %d download retries.", max_retries)
                raise SafeDownloadError(f"Download failed after {max_retries} attempts: {exc}") from exc

            jitter = random.uniform(0.1, 0.5)
            sleep_time = retry_after if retry_after is not None else min(max_backoff, backoff + jitter)
            logger.info("Backing off for %.2f seconds before retry...", sleep_time)
            time.sleep(sleep_time)
            backoff = min(max_backoff, backoff * 2.0)

    raise SafeDownloadError("Max retries exceeded without successful transfer.")


def verify_archive(
    archive_path: Path,
    expected_size: int = EXPECTED_SIZE_BYTES,
    expected_md5: Optional[str] = EXPECTED_MD5,
    requested_url: str = DEFAULT_ARCHIVE_URL,
    final_url: Optional[str] = None,
) -> TransferProvenance:
    """Verify archive size and cryptographic hashes, returning TransferProvenance."""
    archive_path = Path(archive_path).resolve()
    if not archive_path.exists():
        raise FileNotFoundError(f"Archive not found at {archive_path}")

    actual_size = archive_path.stat().st_size
    if actual_size != expected_size:
        raise ChecksumMismatchError(
            f"Archive size mismatch: expected {expected_size} bytes, got {actual_size} bytes."
        )

    md5_hash, sha256_hash = compute_file_hashes(archive_path)

    md5_verified = True
    if expected_md5 is not None:
        if md5_hash.lower() != expected_md5.lower():
            raise ChecksumMismatchError(
                f"MD5 mismatch: expected {expected_md5}, computed {md5_hash}."
            )
    else:
        md5_verified = False

    return TransferProvenance(
        requested_url=requested_url,
        final_url=final_url or requested_url,
        archive_name=archive_path.name,
        file_size_bytes=actual_size,
        expected_size_bytes=expected_size,
        md5_hash=md5_hash,
        expected_md5=expected_md5,
        sha256_hash=sha256_hash,
        download_timestamp_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        status="VERIFIED",
        source_checksum_verified=md5_verified,
        notes="MD5 verified against authoritative Zenodo record metadata; SHA-256 computed for cryptographic provenance.",
    )


def safe_extract_zip(
    archive_path: Path,
    extract_dir: Path,
    overwrite: bool = False,
    max_total_bytes: int = DEFAULT_MAX_TOTAL_UNCOMPRESSED_BYTES,
    max_member_bytes: int = DEFAULT_MAX_SINGLE_MEMBER_BYTES,
) -> List[Dict[str, Any]]:
    """Extract a ZIP archive safely, enforcing cross-platform Zip-Slip containment and size limits.
    
    Generates and saves an extraction manifest with file sizes, status, and SHA-256 hashes.
    """
    archive_path = Path(archive_path).resolve()
    extract_dir = Path(extract_dir).resolve()

    if not archive_path.exists():
        raise FileNotFoundError(f"Archive {archive_path} does not exist.")

    # Check free disk space before extracting
    is_ok, free_gb, req_gb = check_available_disk_space(extract_dir, DEFAULT_REQUIRED_STORAGE_BYTES)
    if not is_ok:
        raise InsufficientDiskSpaceError(
            f"Insufficient disk space for extraction on {extract_dir}: {free_gb:.2f} GB free, {req_gb:.2f} GB required."
        )

    extract_dir.mkdir(parents=True, exist_ok=True)
    manifest: List[Dict[str, Any]] = []

    with zipfile.ZipFile(archive_path, "r") as zf:
        infolist = zf.infolist()

        # Pre-validate all members and check decompression bomb limits
        total_uncompressed = 0
        for member in infolist:
            if not is_safe_zip_member(member.filename, extract_dir):
                raise ZipSlipSecurityError(
                    f"Malicious member path detected: '{member.filename}'. Zip-slip attempt rejected."
                )
            if member.file_size > max_member_bytes:
                raise SafeDownloadError(
                    f"Archive member '{member.filename}' uncompressed size ({member.file_size} bytes) "
                    f"exceeds maximum allowed limit ({max_member_bytes} bytes)."
                )
            total_uncompressed += member.file_size

        if total_uncompressed > max_total_bytes:
            raise SafeDownloadError(
                f"Total uncompressed archive size ({total_uncompressed} bytes) "
                f"exceeds safety threshold ({max_total_bytes} bytes). Decompression bomb rejected."
            )

        # Extraction pass
        for member in infolist:
            clean_rel = member.filename.replace("\\", "/").lstrip("/")
            target_path = (extract_dir / clean_rel).resolve()

            if member.is_dir():
                target_path.mkdir(parents=True, exist_ok=True)
                continue

            target_path.parent.mkdir(parents=True, exist_ok=True)
            file_status = "EXTRACTED"
            if target_path.exists() and not overwrite:
                logger.debug("File %s exists and overwrite=False; skipping extraction.", target_path)
                file_status = "SKIPPED_EXISTING"
            else:
                if target_path.exists() and overwrite:
                    file_status = "OVERWRITTEN"
                with zf.open(member, "r") as src, target_path.open("wb") as dst:
                    while chunk := src.read(1024 * 1024):
                        dst.write(chunk)

            file_sha256 = hashlib.sha256(target_path.read_bytes()).hexdigest()
            manifest.append({
                "relative_path": str(target_path.relative_to(extract_dir)).replace("\\", "/"),
                "size_bytes": target_path.stat().st_size,
                "sha256": file_sha256,
                "status": file_status,
            })

    manifest_file = extract_dir / "extraction_manifest.json"
    manifest_file.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    logger.info("Extracted %d items to %s (manifest saved).", len(manifest), extract_dir)
    return manifest


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="AegisOps safe AnoMod dataset ingestion client.")
    parser.add_argument("--url", default=DEFAULT_ARCHIVE_URL, help="Archive download URL.")
    parser.add_argument("--dest-dir", default=str(DEFAULT_DEST_DIR), help="Destination directory.")
    parser.add_argument("--extract", action="store_true", help="Extract archive upon successful verification.")
    parser.add_argument("--expected-size", type=int, default=EXPECTED_SIZE_BYTES, help="Expected file size in bytes.")
    parser.add_argument("--expected-md5", default=EXPECTED_MD5, help="Expected MD5 checksum from Zenodo metadata.")
    parser.add_argument("--force", action="store_true", help="Force re-download even if archive already exists.")
    parser.add_argument("--dry-run", action="store_true", help="Validate parameters and disk space without downloading.")
    args = parser.parse_args(argv)

    dest_dir = Path(args.dest_dir).resolve()
    archive_path = dest_dir / EXPECTED_ARCHIVE_NAME

    # Measure disk space (require 3.0 GB conservative storage)
    is_ok, free_gb, req_gb = check_available_disk_space(dest_dir, DEFAULT_REQUIRED_STORAGE_BYTES)

    if args.dry_run:
        logger.info("[DRY RUN] Ingestion client verified.")
        logger.info("[DRY RUN] Target URL: %s", args.url)
        logger.info("[DRY RUN] Destination: %s", archive_path)
        logger.info("[DRY RUN] Expected size: %d bytes (%.2f MB).", args.expected_size, args.expected_size / (1024 ** 2))
        logger.info("[DRY RUN] Expected MD5: %s", args.expected_md5)
        logger.info("[DRY RUN] Measured free disk space: %.2f GB (Required: %.2f GB). Status: %s",
                    free_gb, req_gb, "SUFFICIENT" if is_ok else "INSUFFICIENT")
        return 0 if is_ok else 1

    if not is_ok:
        logger.error("Insufficient disk space on %s: %.2f GB free, %.2f GB required.", dest_dir, free_gb, req_gb)
        return 1

    logger.info("Beginning safe ingestion for AnoMod benchmark: %s", args.url)
    try:
        downloaded_path, final_url = download_archive_with_resume(
            url=args.url,
            dest_path=archive_path,
            expected_size=args.expected_size,
            expected_md5=args.expected_md5,
            force=args.force,
        )
        prov = verify_archive(
            archive_path=downloaded_path,
            expected_size=args.expected_size,
            expected_md5=args.expected_md5,
            requested_url=args.url,
            final_url=final_url,
        )
        prov_file = dest_dir / "transfer_provenance.json"
        prov_file.write_text(json.dumps(asdict(prov), indent=2), encoding="utf-8")
        logger.info("Archive verified. SHA-256: %s", prov.sha256_hash)

        if args.extract:
            unpacked_dir = dest_dir / "unpacked"
            safe_extract_zip(downloaded_path, unpacked_dir)

        return 0
    except Exception as exc:
        logger.error("Ingestion failed: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
