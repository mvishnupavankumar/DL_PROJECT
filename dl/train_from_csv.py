from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from dl.anomaly_detector import FEATURES
from dl.live_training import LIVE_MODEL_PATH, train_live_model


def load_healthy_samples(csv_path: str | Path, assume_healthy: bool = False) -> list[dict]:
    df = pd.read_csv(csv_path)
    missing = [feature for feature in FEATURES if feature not in df.columns]
    if missing:
        raise ValueError(f"CSV is missing required feature columns: {missing}. Required order is {list(FEATURES)}.")

    quality_columns = {"fault_mode", "service_available", "status_code", "label"}
    has_quality_metadata = bool(quality_columns.intersection(df.columns))
    if not has_quality_metadata and not assume_healthy:
        raise ValueError("CSV has no health/label columns. Only use known-normal baseline data, then pass --assume-healthy to confirm.")

    if "label" in df.columns:
        labels = pd.to_numeric(df["label"], errors="coerce")
        df = df[labels == 0]
    if "service_available" in df.columns:
        if df["service_available"].dtype == object:
            available = df["service_available"].astype(str).str.lower().isin({"true", "1", "yes"})
        else:
            available = pd.to_numeric(df["service_available"], errors="coerce") == 1
        df = df[available]
    if "status_code" in df.columns:
        df = df[pd.to_numeric(df["status_code"], errors="coerce") == 200]
    if "error_rate_pct" in df.columns and has_quality_metadata:
        # In AegisOps exports this column is both a model feature and a useful quality filter.
        # If the caller explicitly attests that a metadata-free CSV is healthy, retain its feature values.
        df = df[pd.to_numeric(df["error_rate_pct"], errors="coerce") == 0]
    if "fault_mode" in df.columns:
        df = df[df["fault_mode"].astype(str).str.lower() == "normal"]

    for feature in FEATURES:
        df[feature] = pd.to_numeric(df[feature], errors="coerce")
    df = df.dropna(subset=list(FEATURES))
    df = df[[*FEATURES]].replace([float("inf"), float("-inf")], pd.NA).dropna()
    # Exclude obvious resource/latency incidents from the normal-only training baseline.
    df = df[(df["cpu_pct"] < 90) & (df["memory_pct"] < 95) & (df["latency_ms"] < 1000) & (df["disk_pct"] < 95)]
    return df.to_dict(orient="records")


def main() -> None:
    parser = argparse.ArgumentParser(description="Train the AegisOps LSTM model from a five-feature telemetry CSV.")
    parser.add_argument("--csv", required=True, help="CSV exported from AegisOps Live Monitoring or a compatible telemetry source")
    parser.add_argument("--output", default=str(LIVE_MODEL_PATH))
    parser.add_argument("--epochs", type=int, default=12)
    parser.add_argument("--min-samples", type=int, default=180)
    parser.add_argument("--assume-healthy", action="store_true", help="Confirm that an unlabelled CSV contains only healthy baseline observations")
    args = parser.parse_args()

    samples = load_healthy_samples(args.csv, assume_healthy=args.assume_healthy)
    result = train_live_model(
        samples,
        output_path=args.output,
        epochs=args.epochs,
        min_samples=args.min_samples,
        data_source=f"User-provided telemetry CSV: {Path(args.csv).resolve()}",
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
