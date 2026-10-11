import numpy as np
import pytest

from dl.anomaly_detector import (
    DEFAULT_MODEL_PATH,
    FEATURES,
    generate_incident_telemetry,
    generate_normal_windows,
    load_detector,
)


@pytest.fixture(scope="module")
def detector():
    if not DEFAULT_MODEL_PATH.exists():
        pytest.skip("Run `python -m dl.train_model` before testing the trained model.")
    return load_detector()


def test_normal_telemetry_shape_and_values():
    values = generate_normal_windows(4, seed=9)
    assert values.shape == (4, 24, len(FEATURES))
    assert np.isfinite(values).all()


def test_detector_returns_expected_fields(detector):
    window, _ = generate_incident_telemetry("INC-1001")
    result = detector.detect(window)
    assert {"is_anomaly", "score", "threshold", "flagged_features", "latest_metrics"} <= result.keys()
    assert result["score"] >= 0
    assert result["threshold"] > 0


@pytest.mark.parametrize("incident_id", [
    "INC-1001", "INC-1002", "INC-1003", "INC-1004", "INC-1005", "INC-1006"
])
def test_all_injected_incident_profiles_trigger_detection(detector, incident_id):
    window, _ = generate_incident_telemetry(incident_id)
    result = detector.detect(window)
    assert result["is_anomaly"], f"{incident_id} did not cross the anomaly threshold: {result['score']} <= {result['threshold']}"


def test_detector_rejects_wrong_shape(detector):
    with pytest.raises(ValueError):
        detector.detect(np.zeros((24, 2), dtype=np.float32))
