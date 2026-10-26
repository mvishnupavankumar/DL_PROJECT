#!/usr/bin/env python3
"""Read-only structural validation for the Phase 4.1 figure set.

The generated PDFs are Pillow single-image PDFs.  This utility extracts the
embedded DCT page image for independent page-payload inspection; it neither
rewrites a figure nor changes evidence inputs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image, ImageChops, ImageStat


HERE = Path(__file__).resolve().parent


def extract_pdf_dct(pdf: Path, destination: Path) -> None:
    payload = pdf.read_bytes()
    marker = payload.index(b"/DCTDecode")
    start = payload.index(b"stream\n", marker) + len(b"stream\n")
    end = payload.index(b"\nendstream", start)
    destination.write_bytes(payload[start:end])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf-review-dir", type=Path, required=True)
    args = parser.parse_args()
    args.pdf_review_dir.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((HERE / "PHASE4_SHA256_MANIFEST.json").read_text(encoding="utf-8"))
    mismatches = []
    for item in manifest["files"]:
        path = HERE / item["path"]
        if not path.is_file() or path.stat().st_size != item["bytes"] or hashlib.sha256(path.read_bytes()).hexdigest() != item["sha256"]:
            mismatches.append(item["path"])
    records = []
    for png in sorted(HERE.glob("FIG_*.png")):
        svg = png.with_suffix(".svg")
        pdf = png.with_suffix(".pdf")
        ET.parse(svg)
        original = Image.open(png).convert("RGB")
        extracted = args.pdf_review_dir / f"{png.stem}_pdf-page.jpg"
        extract_pdf_dct(pdf, extracted)
        pdf_image = Image.open(extracted).convert("RGB")
        if original.size != (1800, 1125) or pdf_image.size != original.size:
            raise ValueError(f"Unexpected page dimensions for {png.name}")
        difference = ImageStat.Stat(ImageChops.difference(original, pdf_image)).mean
        records.append({"figure": png.stem, "png": original.size, "pdf_page": pdf_image.size, "mean_rgb_delta": [round(x, 3) for x in difference]})
    if mismatches:
        raise ValueError("Manifest mismatch: " + ", ".join(mismatches))
    print(json.dumps({"figures": len(records), "manifest_entries": len(manifest["files"]), "manifest_mismatches": mismatches, "records": records}, indent=2))


if __name__ == "__main__":
    main()
