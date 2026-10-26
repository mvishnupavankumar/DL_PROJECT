"""Read-only Phase 9 semantic and raster checks for the five staged assets."""

from __future__ import annotations

import csv
import io
import json
from collections import Counter
from pathlib import Path
import xml.etree.ElementTree as ET

from PIL import Image


ROOT = Path(__file__).resolve().parents[3]
STAGING = ROOT / "research" / "exports" / "phase9" / "staging"
BACKUPS = ROOT / "research" / "exports" / "phase9" / "backups" / "pre-remediation"
PHASE4 = ROOT / "research" / "figures" / "phase4"
TARGETS = (
    "FIG_B_FROZEN_LSTM.png",
    "FIG_D_DIAGNOSIS_APPROVAL.png",
    "FIG_E2_CONFUSION_MATRICES.png",
    "FIG_E4_DIAGNOSIS_PILOT.png",
    "FIG_E6_LIVE_EVIDENCE.png",
)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def pixel_bounds(image: Image.Image, y_start: int, y_end: int) -> tuple[int, int]:
    image = image.convert("RGB")
    pixels = image.load()
    xs = [
        x
        for y in range(y_start, y_end)
        for x in range(image.width)
        if pixels[x, y] != (255, 255, 255)
    ]
    return min(xs), max(xs)


def embedded_pdf_image(pdf: Path) -> Image.Image:
    payload = pdf.read_bytes()
    marker = payload.index(b"/DCTDecode")
    start = payload.index(b"stream\n", marker) + len(b"stream\n")
    end = payload.index(b"\nendstream", start)
    return Image.open(io.BytesIO(payload[start:end])).convert("RGB")


def main() -> None:
    a = csv_rows(ROOT / "research" / "raw" / "detection_predictions.csv")
    b = csv_rows(ROOT / "research" / "raw" / "diagnosis_predictions.csv")
    live = csv_rows(ROOT / "research" / "exports" / "telemetry.csv")

    expected_confusion = {
        "rule_flag": [120, 0, 200, 0],
        "iso_flag": [57, 4, 196, 63],
        "lstm_flag": [120, 2, 198, 0],
        "combined_flag": [120, 2, 198, 0],
    }
    confusion = {}
    for column, expected in expected_confusion.items():
        counts = [
            sum(row["ground_truth"] == truth and row[column] == prediction for row in a)
            for truth, prediction in (("1", "1"), ("0", "1"), ("0", "0"), ("1", "0"))
        ]
        assert counts == expected, (column, counts, expected)
        confusion[column] = {"tp": counts[0], "fp": counts[1], "tn": counts[2], "fn": counts[3]}

    configurations = list(dict.fromkeys(row["configuration"] for row in b))
    diagnosis = []
    for configuration in configurations:
        rows = [row for row in b if row["configuration"] == configuration]
        strict = sum(row["top1_strict"] == "1" for row in rows)
        assessable = sum(row["rubric_verdict"] != "UNASSESSABLE" for row in rows)
        completed = sum(
            row["top1_strict"] == "1" and row["rubric_verdict"] != "UNASSESSABLE" for row in rows
        )
        assert len(rows) == 6, (configuration, len(rows))
        diagnosis.append(
            {
                "configuration": configuration,
                "strict": strict,
                "intent_to_treat_denominator": len(rows),
                "completed": completed,
                "completed_case_denominator": assessable,
                "unassessable": len(rows) - assessable,
            }
        )
    assert [(row["strict"], row["completed"], row["completed_case_denominator"], row["unassessable"]) for row in diagnosis] == [
        (6, 6, 6, 0), (3, 3, 6, 0), (3, 3, 6, 0), (6, 6, 6, 0),
        (4, 4, 5, 1), (5, 5, 6, 0), (4, 4, 5, 1),
    ]

    modes = Counter(row["detector_mode"] for row in live)
    faults = Counter(row["fault_mode"] for row in live)
    null_scores = sum(not row["anomaly_score"].strip() for row in live)
    assert len(a) == 320
    assert len(b) == 42
    assert len(live) == 200
    assert modes == {"bootstrap_rules": 200}
    assert null_scores == 200
    assert faults == {"error": 168, "latency": 1, "normal": 31}

    raster = {}
    for name in TARGETS:
        image = Image.open(STAGING / name).convert("RGB")
        assert image.size == (1800, 1125), (name, image.size)
        header = pixel_bounds(image, 25, 150)
        footer = pixel_bounds(image, 985, 1120)
        assert header[0] >= 120, (name, "header", header)
        assert footer[0] >= 120, (name, "footer", footer)
        raster[name] = {"dimensions": list(image.size), "header_nonwhite_x": list(header), "footer_nonwhite_x": list(footer)}

    vector_and_pdf = {}
    for name in TARGETS:
        stem = Path(name).stem
        ET.parse(PHASE4 / f"{stem}.svg")
        original = Image.open(BACKUPS / name).convert("RGB")
        pdf_image = embedded_pdf_image(PHASE4 / f"{stem}.pdf")
        assert original.size == pdf_image.size == (1800, 1125), (name, original.size, pdf_image.size)
        vector_and_pdf[name] = {"svg_parse": "pass", "pdf_embedded_page_dimensions": list(pdf_image.size)}

    print(json.dumps({
        "result": "pass",
        "experiment_a_rows": len(a),
        "experiment_a_confusion": confusion,
        "experiment_b_rows": len(b),
        "experiment_b_configurations": diagnosis,
        "live": {"rows": len(live), "modes": dict(modes), "null_lstm_scores": null_scores, "fault_modes": dict(faults)},
        "staged_raster": raster,
        "unchanged_svg_pdf": vector_and_pdf,
    }, indent=2))


if __name__ == "__main__":
    main()
