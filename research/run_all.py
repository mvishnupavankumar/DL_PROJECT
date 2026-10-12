#!/usr/bin/env python3
"""Unified, reproducible research pipeline runner for AegisOps."""
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from research.experiments.run_experiment_a import run_experiment_a
from research.experiments.run_experiment_b import run_experiment_b
from research.experiments.run_experiment_c import run_experiment_c

def compute_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def generate_manifest():
    print("\nGenerating SHA-256 Artifact & Model Manifest...")
    manifest_files = [
        ROOT / "models" / "lstm_autoencoder.pt",
        ROOT / "models" / "lstm_autoencoder.json",
        ROOT / "data" / "aegisops_live.sqlite3",
        ROOT / "data" / "incidents.json",
        ROOT / "research" / "PROJECT_VERSION_AND_ENVIRONMENT.md",
        ROOT / "research" / "DATA_AND_LABEL_AUDIT.md",
        ROOT / "research" / "STATISTICAL_AUDIT.md",
        ROOT / "research" / "SAFETY_EVALUATION.md",
        ROOT / "research" / "FINAL_EXPERIMENT_REPORT.md",
        ROOT / "research" / "raw" / "detection_metrics.csv",
        ROOT / "research" / "raw" / "detection_predictions.csv",
        ROOT / "research" / "raw" / "diagnosis_metrics.csv",
        ROOT / "research" / "raw" / "diagnosis_predictions.csv",
        ROOT / "research" / "raw" / "safety_metrics.csv",
        ROOT / "research" / "raw" / "safety_test_results.csv",
        ROOT / "research" / "audits" / "REPOSITORY_AUDIT.md",
        ROOT / "research" / "audits" / "DATABASE_AUDIT.md",
        ROOT / "research" / "audits" / "MODEL_AND_EXECUTION_AUDIT.md",
        ROOT / "research" / "audits" / "TEST_RESULTS.md",
        ROOT / "research" / "audits" / "PHASE_1_VERDICT.md",
        ROOT / "research" / "figures" / "detection_confusion_matrices.png",
        ROOT / "research" / "figures" / "detection_comparison.png",
    ]
    manifest = {
        "manifest_version": "2.0.0",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "project_root": str(ROOT),
        "artifacts": {}
    }
    for p in manifest_files:
        if p.exists():
            manifest["artifacts"][p.name] = {
                "relative_path": str(p.relative_to(ROOT)).replace("\\", "/"),
                "size_bytes": p.stat().st_size,
                "sha256": compute_sha256(p)
            }
        else:
            manifest["artifacts"][p.name] = {"status": "MISSING"}
            
    out_manifest = ROOT / "research" / "MANIFEST_SHA256.json"
    out_manifest.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Saved manifest: {out_manifest}")

def main():
    print("=" * 80)
    print("AEGISOPS UNIFIED EXPERIMENT & REPRODUCIBILITY SUITE")
    print("=" * 80)
    start_total = time.perf_counter()

    # Step 1: Run pytest regression suite
    print("\n[Step 1/5] Running Pytest Regression Suite (42 tests)...")
    res = subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=ROOT, capture_output=True, text=True)
    print(res.stdout.strip())
    if res.returncode != 0:
        print("Tests failed:", res.stderr)
        return res.returncode

    # Step 2: Run Experiment A (Anomaly Detection)
    print("\n[Step 2/5] Running Experiment A (Anomaly Detection & Figure Generation)...")
    run_experiment_a()
    plot_script = ROOT / "research" / "experiments" / "plot_detection_figures.py"
    subprocess.run([sys.executable, str(plot_script)], cwd=ROOT, check=True)

    # Step 3: Run Experiment B (Root-Cause Diagnosis Rubric Audit)
    print("\n[Step 3/5] Running Experiment B (Diagnosis Rubric Evaluation)...")
    diag_script = ROOT / "research" / "experiments" / "generate_diagnosis_audit.py"
    subprocess.run([sys.executable, str(diag_script)], cwd=ROOT, check=True)

    # Step 4: Run Experiment C (Safety & Verification on Live FastAPI Service)
    print("\n[Step 4/5] Running Experiment C (Safety & Verification Audit)...")
    safety_script = ROOT / "research" / "experiments" / "run_safety_audit.py"
    subprocess.run([sys.executable, str(safety_script)], cwd=ROOT, check=True)

    # Step 5: Statistical Analysis & Manifest
    print("\n[Step 5/5] Generating Statistical Analysis & Checksum Manifest...")
    stat_script = ROOT / "research" / "results" / "generate_statistical_analysis.py"
    subprocess.run([sys.executable, str(stat_script)], cwd=ROOT, check=True)
    generate_manifest()

    elapsed = time.perf_counter() - start_total
    print("\n" + "=" * 80)
    print(f"ALL EXPERIMENTS AND AUDITS COMPLETED SUCCESSFULLY IN {elapsed:.1f} SECONDS")
    print("=" * 80)
    return 0

if __name__ == "__main__":
    sys.exit(main())
