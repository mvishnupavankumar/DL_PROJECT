from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL_PATH = ROOT / "models" / "lstm_autoencoder.pt"
FEATURES = ("cpu_pct", "memory_pct", "latency_ms", "error_rate_pct", "disk_pct")
SEQUENCE_LENGTH = 24
HIDDEN_SIZE = 16


class LSTMAutoencoder(nn.Module):
    """Sequence autoencoder that learns normal IT telemetry patterns."""

    def __init__(self, n_features: int = len(FEATURES), hidden_size: int = HIDDEN_SIZE):
        super().__init__()
        self.encoder = nn.LSTM(n_features, hidden_size, batch_first=True)
        self.decoder = nn.LSTM(hidden_size, hidden_size, batch_first=True)
        self.output_layer = nn.Linear(hidden_size, n_features)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        _, (hidden, _) = self.encoder(x)
        latent = hidden[-1].unsqueeze(1).repeat(1, x.size(1), 1)
        decoded, _ = self.decoder(latent)
        return self.output_layer(decoded)


def generate_normal_windows(
    n_windows: int = 800,
    sequence_length: int = SEQUENCE_LENGTH,
    seed: int = 42,
) -> np.ndarray:
    """Generate reproducible, normal-only telemetry for a self-contained demo."""
    rng = np.random.default_rng(seed)
    t = np.arange(sequence_length, dtype=np.float32)
    data = np.zeros((n_windows, sequence_length, len(FEATURES)), dtype=np.float32)

    for i in range(n_windows):
        phase = rng.uniform(0, 2 * np.pi)
        cpu_base = rng.normal(42, 4)
        mem_base = rng.normal(54, 3)
        disk_base = rng.normal(47, 4)
        cpu = cpu_base + 5.0 * np.sin(t / 4 + phase) + rng.normal(0, 2.2, sequence_length)
        memory = mem_base + 1.8 * np.sin(t / 7 + phase / 2) + np.cumsum(
            rng.normal(0, 0.22, sequence_length)
        ) + rng.normal(0, 1.0, sequence_length)
        latency = 42 + 0.60 * cpu + 0.18 * memory + rng.normal(0, 5.0, sequence_length)
        errors = 0.24 + np.maximum(cpu - 62, 0) * 0.035 + rng.normal(0, 0.055, sequence_length)
        disk = disk_base + 0.11 * t + rng.normal(0, 1.5, sequence_length)

        data[i, :, 0] = np.clip(cpu, 15, 75)
        data[i, :, 1] = np.clip(memory, 35, 75)
        data[i, :, 2] = np.clip(latency, 35, 160)
        data[i, :, 3] = np.clip(errors, 0.02, 1.2)
        data[i, :, 4] = np.clip(disk, 25, 75)

    return data


def generate_incident_telemetry(incident_id: str, seed: int = 100) -> tuple[np.ndarray, str]:
    """Create a deterministic synthetic telemetry window for an incident scenario."""
    window = generate_normal_windows(1, seed=seed)[0].copy()
    tail = 8
    label = "Injected incident telemetry"

    if incident_id == "INC-1001":
        window[-tail:, 2] = np.linspace(220, 760, tail)
        window[-tail:, 3] = np.linspace(3.0, 28.0, tail)
        label = "Payment API: connection-pool exhaustion / HTTP 500"
    elif incident_id == "INC-1002":
        window[-tail:, 0] = np.linspace(38, 16, tail)
        window[-tail:, 2] = np.linspace(220, 1250, tail)
        window[-tail:, 3] = np.linspace(2.0, 55.0, tail)
        label = "Customer database: unavailable service / connection refused"
    elif incident_id == "INC-1003":
        window[-tail:, 0] = np.linspace(82, 99, tail)
        window[-tail:, 1] = np.linspace(70, 91, tail)
        window[-tail:, 2] = np.linspace(100, 380, tail)
        window[-tail:, 3] = np.linspace(1.0, 14.0, tail)
        label = "Production server: CPU saturation"
    elif incident_id == "INC-1004":
        window[-tail:, 4] = np.linspace(82, 99.5, tail)
        window[-tail:, 3] = np.linspace(0.6, 20.0, tail)
        window[-tail:, 2] = np.linspace(100, 260, tail)
        label = "Server storage: disk capacity exhausted"
    elif incident_id == "INC-1005":
        window[-tail:, 2] = np.linspace(90, 280, tail)
        window[-tail:, 3] = np.linspace(1.0, 24.0, tail)
        label = "Authentication: token validation failures"
    elif incident_id == "INC-1006":
        window[-tail:, 2] = np.linspace(160, 1150, tail)
        window[-tail:, 3] = np.linspace(1.0, 16.0, tail)
        label = "Internal API: service-to-service timeouts"

    return window.astype(np.float32), label


class TelemetryAnomalyDetector:
    def __init__(
        self,
        model: LSTMAutoencoder,
        mean: np.ndarray,
        std: np.ndarray,
        threshold: float,
        feature_thresholds: np.ndarray,
        sequence_length: int = SEQUENCE_LENGTH,
        features: tuple[str, ...] | list[str] = FEATURES,
        data_source: str = "Synthetic demo telemetry",
    ):
        self.model = model.eval()
        self.mean = np.asarray(mean, dtype=np.float32)
        self.std = np.maximum(np.asarray(std, dtype=np.float32), 1e-6)
        self.threshold = float(threshold)
        self.feature_thresholds = np.asarray(feature_thresholds, dtype=np.float32)
        self.sequence_length = int(sequence_length)
        self.features = tuple(features)
        self.data_source = str(data_source)

    @classmethod
    def load(cls, path: str | Path = DEFAULT_MODEL_PATH) -> "TelemetryAnomalyDetector":
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(
                f"Trained model not found at {path}. Run: python -m dl.train_model"
            )
        checkpoint = torch.load(path, map_location="cpu", weights_only=True)
        model = LSTMAutoencoder(
            n_features=len(checkpoint["features"]),
            hidden_size=int(checkpoint["hidden_size"]),
        )
        model.load_state_dict(checkpoint["state_dict"])
        return cls(
            model=model,
            mean=np.asarray(checkpoint["mean"], dtype=np.float32),
            std=np.asarray(checkpoint["std"], dtype=np.float32),
            threshold=checkpoint["threshold"],
            feature_thresholds=np.asarray(checkpoint["feature_thresholds"], dtype=np.float32),
            sequence_length=checkpoint["sequence_length"],
            features=tuple(checkpoint.get("features", FEATURES)),
            data_source=checkpoint.get("data_source", "Synthetic demo telemetry"),
        )

    def detect(self, telemetry: np.ndarray) -> dict[str, Any]:
        values = np.asarray(telemetry, dtype=np.float32)
        if values.ndim != 2 or values.shape[1] != len(self.features):
            raise ValueError(f"Telemetry must have shape (time_steps, {len(self.features)} features).")
        if values.shape[0] != self.sequence_length:
            raise ValueError(f"Expected {self.sequence_length} time steps; received {values.shape[0]}.")
        if not np.isfinite(values).all():
            raise ValueError("Telemetry contains NaN or infinite values.")

        normalized = (values - self.mean) / self.std
        x = torch.from_numpy(normalized).unsqueeze(0)
        with torch.no_grad():
            reconstructed = self.model(x).squeeze(0).cpu().numpy()

        squared_errors = np.square(reconstructed - normalized)
        score = float(squared_errors.mean())
        feature_errors = squared_errors.mean(axis=0)
        flagged = [
            {
                "feature": self.features[i],
                "reconstruction_error": float(feature_errors[i]),
                "threshold": float(self.feature_thresholds[i]),
            }
            for i in range(len(self.features))
            if feature_errors[i] > self.feature_thresholds[i]
        ]
        latest = {self.features[i]: float(values[-1, i]) for i in range(len(self.features))}
        return {
            "is_anomaly": score > self.threshold,
            "score": score,
            "threshold": self.threshold,
            "severity": "HIGH" if score > self.threshold * 3 else ("MEDIUM" if score > self.threshold else "NORMAL"),
            "flagged_features": flagged,
            "feature_errors": {self.features[i]: float(feature_errors[i]) for i in range(len(self.features))},
            "latest_metrics": latest,
            "model": "LSTM Autoencoder",
            "data_source": self.data_source,
        }


def train_and_save_model(
    output_path: str | Path = DEFAULT_MODEL_PATH,
    n_windows: int = 800,
    epochs: int = 18,
    seed: int = 42,
) -> dict[str, Any]:
    """Train on normal synthetic telemetry and calibrate reconstruction thresholds."""
    torch.manual_seed(seed)
    np.random.seed(seed)
    torch.set_num_threads(1)

    windows = generate_normal_windows(n_windows=n_windows, seed=seed)
    split = max(1, int(len(windows) * 0.85))
    train, validation = windows[:split], windows[split:]
    mean = train.reshape(-1, len(FEATURES)).mean(axis=0)
    std = train.reshape(-1, len(FEATURES)).std(axis=0)
    std = np.maximum(std, 1e-6)
    train_scaled = (train - mean) / std
    validation_scaled = (validation - mean) / std

    train_tensor = torch.from_numpy(train_scaled.astype(np.float32))
    loader = DataLoader(TensorDataset(train_tensor), batch_size=64, shuffle=True)
    model = LSTMAutoencoder()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.003)
    loss_fn = nn.MSELoss()
    losses: list[float] = []

    for _ in range(epochs):
        model.train()
        batch_losses = []
        for (batch,) in loader:
            optimizer.zero_grad(set_to_none=True)
            output = model(batch)
            loss = loss_fn(output, batch)
            loss.backward()
            optimizer.step()
            batch_losses.append(float(loss.detach()))
        losses.append(float(np.mean(batch_losses)))

    model.eval()
    with torch.no_grad():
        val_x = torch.from_numpy(validation_scaled.astype(np.float32))
        val_reconstructed = model(val_x).numpy()
    val_errors = np.square(val_reconstructed - validation_scaled)
    val_scores = val_errors.mean(axis=(1, 2))
    feature_errors = val_errors.mean(axis=1)
    threshold = float(np.quantile(val_scores, 0.99))
    feature_thresholds = np.quantile(feature_errors, 0.99, axis=0).astype(np.float32)

    checkpoint = {
        "state_dict": model.state_dict(),
        "mean": mean.astype(np.float32).tolist(),
        "std": std.astype(np.float32).tolist(),
        "threshold": threshold,
        "feature_thresholds": feature_thresholds.tolist(),
        "features": list(FEATURES),
        "sequence_length": SEQUENCE_LENGTH,
        "data_source": "Synthetic demo telemetry",
        "hidden_size": HIDDEN_SIZE,
        "epochs": epochs,
        "training_windows": int(len(train)),
        "validation_windows": int(len(validation)),
        "final_training_loss": float(losses[-1]),
        "threshold_method": "99th percentile of held-out normal reconstruction error",
    }
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(checkpoint, output_path)
    metadata_path = output_path.with_suffix(".json")
    metadata_path.write_text(json.dumps({k: v for k, v in checkpoint.items() if k != "state_dict"}, indent=2), encoding="utf-8")
    return {
        "model_path": str(output_path),
        "metadata_path": str(metadata_path),
        "training_windows": int(len(train)),
        "validation_windows": int(len(validation)),
        "epochs": epochs,
        "final_training_loss": float(losses[-1]),
        "threshold": threshold,
    }


def load_detector(path: str | Path = DEFAULT_MODEL_PATH) -> TelemetryAnomalyDetector:
    return TelemetryAnomalyDetector.load(path)
