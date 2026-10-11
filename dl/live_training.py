from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from dl.anomaly_detector import FEATURES, HIDDEN_SIZE, LSTMAutoencoder, SEQUENCE_LENGTH, TelemetryAnomalyDetector

ROOT = Path(__file__).resolve().parents[1]
LIVE_MODEL_PATH = ROOT / "models" / "live_lstm_autoencoder.pt"


def _windows(rows: np.ndarray, sequence_length: int) -> np.ndarray:
    if len(rows) < sequence_length:
        return np.empty((0, sequence_length, rows.shape[1]), dtype=np.float32)
    return np.stack([rows[i:i + sequence_length] for i in range(len(rows) - sequence_length + 1)]).astype(np.float32)


def train_live_model(samples: list[dict[str, Any]], output_path: str | Path = LIVE_MODEL_PATH,
                     epochs: int = 12, min_samples: int = 180, seed: int = 37,
                     data_source: str = "Real live telemetry collected from local host and AegisOps test service") -> dict[str, Any]:
    """Train using only chronologically split, healthy telemetry recorded by the live collector."""
    if len(samples) < min_samples:
        raise ValueError(
            f"Need at least {min_samples} healthy live samples; found {len(samples)}. "
            "Keep AegisOps collecting while the local test service is healthy."
        )
    rows = np.asarray([[float(s[f]) for f in FEATURES] for s in samples], dtype=np.float32)
    if not np.isfinite(rows).all():
        raise ValueError("Healthy telemetry contains non-finite values; clean it before training.")
    split = int(len(rows) * 0.8)
    train_rows, val_rows = rows[:split], rows[split:]
    if len(train_rows) < SEQUENCE_LENGTH * 3 or len(val_rows) < SEQUENCE_LENGTH + 5:
        raise ValueError("Not enough data in chronological training/validation splits; collect more healthy samples.")

    mean = train_rows.mean(axis=0)
    # Domain-aware floors stop almost-constant metrics (disk or error rate) from getting
    # enormous normalized scores due to tiny floating-point standard deviations.
    std_floors = np.asarray([1.0, 0.5, 5.0, 0.5, 0.5], dtype=np.float32)
    std = np.maximum(train_rows.std(axis=0), std_floors)
    train_scaled = (train_rows - mean) / std
    val_scaled = (val_rows - mean) / std
    train_windows = _windows(train_scaled, SEQUENCE_LENGTH)
    val_windows = _windows(val_scaled, SEQUENCE_LENGTH)
    if len(train_windows) < 20 or len(val_windows) < 5:
        raise ValueError("Not enough sequence windows for a stable calibration; collect more samples.")

    torch.manual_seed(seed)
    np.random.seed(seed)
    torch.set_num_threads(1)
    loader = DataLoader(TensorDataset(torch.from_numpy(train_windows)), batch_size=32, shuffle=True)
    model = LSTMAutoencoder(n_features=len(FEATURES), hidden_size=HIDDEN_SIZE)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.002)
    loss_fn = nn.MSELoss()
    losses: list[float] = []
    for _ in range(max(1, int(epochs))):
        model.train()
        batch_losses = []
        for (batch,) in loader:
            optimizer.zero_grad(set_to_none=True)
            pred = model(batch)
            loss = loss_fn(pred, batch)
            loss.backward()
            optimizer.step()
            batch_losses.append(float(loss.detach()))
        losses.append(float(np.mean(batch_losses)))

    model.eval()
    with torch.no_grad():
        val_pred = model(torch.from_numpy(val_windows)).numpy()
    errors = np.square(val_pred - val_windows)
    scores = errors.mean(axis=(1, 2))
    feature_errors = errors.mean(axis=1)
    threshold = float(np.quantile(scores, 0.99))
    feature_thresholds = np.quantile(feature_errors, 0.99, axis=0).astype(np.float32)
    checkpoint = {
        "state_dict": model.state_dict(),
        "mean": mean.astype(np.float32).tolist(),
        "std": std.astype(np.float32).tolist(),
        "threshold": threshold,
        "feature_thresholds": feature_thresholds.tolist(),
        "features": list(FEATURES),
        "sequence_length": SEQUENCE_LENGTH,
        "hidden_size": HIDDEN_SIZE,
        "epochs": max(1, int(epochs)),
        "training_samples": int(len(train_rows)),
        "validation_samples": int(len(val_rows)),
        "training_windows": int(len(train_windows)),
        "validation_windows": int(len(val_windows)),
        "final_training_loss": losses[-1],
        "data_source": data_source,
        "threshold_method": "99th percentile of chronologically held-out healthy validation windows",
    }
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(checkpoint, output_path)
    metadata_path = output_path.with_suffix(".json")
    metadata_path.write_text(json.dumps({k: v for k, v in checkpoint.items() if k != "state_dict"}, indent=2), encoding="utf-8")
    return {k: v for k, v in checkpoint.items() if k not in {"state_dict", "mean", "std", "feature_thresholds"}} | {
        "model_path": str(output_path), "metadata_path": str(metadata_path), "threshold": threshold
    }


def load_live_detector() -> TelemetryAnomalyDetector:
    return TelemetryAnomalyDetector.load(LIVE_MODEL_PATH)
