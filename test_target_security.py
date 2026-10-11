from collectors.system_metrics import validate_local_service_url, validate_monitoring_target_url
import pytest


def test_remote_https_target_is_allowed_for_monitoring():
    assert validate_monitoring_target_url("https://status.example.org") == "https://status.example.org"


def test_remote_http_target_is_rejected():
    with pytest.raises(ValueError):
        validate_monitoring_target_url("http://status.example.org")


def test_credentials_in_url_are_rejected():
    with pytest.raises(ValueError):
        validate_monitoring_target_url("https://user:secret@example.org")


def test_remote_target_never_passes_local_remediation_gate():
    with pytest.raises(ValueError):
        validate_local_service_url("https://status.example.org")
