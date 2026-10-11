from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import psutil
import requests

from storage.telemetry_store import TelemetryStore

DEFAULT_SERVICE_URL = os.getenv("AEGISOPS_SERVICE_URL", "http://127.0.0.1:8765").rstrip("/")
PROBE_PATH = os.getenv("AEGISOPS_PROBE_PATH", "/probe")
REQUEST_TIMEOUT_S = float(os.getenv("AEGISOPS_REQUEST_TIMEOUT_S", "3.0"))
VERIFY_TLS = os.getenv("AEGISOPS_VERIFY_TLS", "true").strip().lower() not in {"0", "false", "no"}
BEARER_TOKEN = os.getenv("AEGISOPS_BEARER_TOKEN", "").strip()


def validate_local_service_url(service_url: str) -> str:
    """Safety boundary for test-service fault injection and remediation."""
    parsed = urlparse(service_url)
    if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise ValueError("Remediation and fault injection are restricted to HTTP on localhost.")
    if not parsed.port:
        raise ValueError("The local test service URL must include a port, e.g. http://127.0.0.1:8765.")
    return service_url.rstrip("/")


def validate_monitoring_target_url(service_url: str) -> str:
    """Validate an explicitly configured monitoring target.

    Remote targets must use HTTPS. Plain HTTP is allowed only for localhost.
    This function does not authorize any write/remediation operation.
    """
    parsed = urlparse(service_url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Target must be a full HTTP(S) URL.")
    local_hosts = {"127.0.0.1", "localhost", "::1"}
    if parsed.scheme == "http" and parsed.hostname not in local_hosts:
        raise ValueError("Remote monitoring targets must use HTTPS; HTTP is allowed only on localhost.")
    if parsed.username or parsed.password:
        raise ValueError("Do not embed credentials in a URL; configure AEGISOPS_BEARER_TOKEN instead.")
    if parsed.query or parsed.fragment:
        raise ValueError("Configure a base URL without query parameters or fragments.")
    return service_url.rstrip("/")


def _disk_usage_percent() -> float:
    anchor = Path.cwd().anchor or ("C:\\" if os.name == "nt" else "/")
    try:
        return float(psutil.disk_usage(anchor).percent)
    except (OSError, ValueError):
        return float(psutil.disk_usage("/").percent)


def _headers() -> dict[str, str]:
    headers = {"User-Agent": "AegisOps-Monitor/1.0"}
    if BEARER_TOKEN:
        headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
    return headers


def collect_live_sample(
    store: TelemetryStore,
    service_url: str = DEFAULT_SERVICE_URL,
    timeout_s: float = REQUEST_TIMEOUT_S,
) -> dict[str, Any]:
    """Capture collector-host metrics and a timed HTTP probe to the configured target.

    CPU/memory/disk values describe the machine running the collector, not a remote
    target. Remote host metrics require an agent/exporter or an authenticated metrics API.
    """
    service_url = validate_monitoring_target_url(service_url)
    path = PROBE_PATH if PROBE_PATH.startswith("/") else f"/{PROBE_PATH}"
    probe_url = f"{service_url}{path}"
    cpu = float(psutil.cpu_percent(interval=0.15))
    memory = float(psutil.virtual_memory().percent)
    disk = _disk_usage_percent()
    start = time.perf_counter()
    status_code = 0
    error_message = ""
    service_available = False
    fault_mode = "unknown"
    try:
        response = requests.get(
            probe_url,
            timeout=max(0.2, float(timeout_s)),
            headers=_headers(),
            verify=VERIFY_TLS,
            allow_redirects=False,
        )
        status_code = int(response.status_code)
        service_available = status_code == 200
        if not service_available:
            error_message = f"Probe returned HTTP {status_code}"
        try:
            probe_body = response.json()
            fault_mode = str(probe_body.get("fault_mode", "unknown"))
        except (ValueError, AttributeError):
            pass
    except requests.RequestException as exc:
        error_message = f"{type(exc).__name__}: {exc}"
    latency_ms = float((time.perf_counter() - start) * 1000)

    # Local test service exposes fault_mode; remote services generally do not.
    if fault_mode == "unknown" and service_url.startswith(("http://127.0.0.1:", "http://localhost:", "http://[::1]:")):
        try:
            health = requests.get(
                f"{service_url}/health",
                timeout=max(0.2, float(timeout_s)),
                headers=_headers(),
                verify=VERIFY_TLS,
                allow_redirects=False,
            )
            if health.ok:
                fault_mode = str(health.json().get("fault_mode", "unknown"))
        except (requests.RequestException, ValueError):
            pass

    previous = store.recent_probe_outcomes(limit=19)
    outcomes = [int(item) for item in previous] + [status_code]
    error_rate = 100.0 * sum(code != 200 for code in outcomes) / max(len(outcomes), 1)
    sample = {
        "timestamp": store.now_iso(),
        "cpu_pct": round(cpu, 4),
        "memory_pct": round(memory, 4),
        "latency_ms": round(latency_ms, 4),
        "error_rate_pct": round(error_rate, 4),
        "disk_pct": round(disk, 4),
        "service_available": bool(service_available),
        "status_code": int(status_code),
        "error_message": error_message,
        "fault_mode": fault_mode,
        "data_source": "live_local_host_and_http_probe" if service_url.startswith(("http://127.0.0.1:", "http://localhost:", "http://[::1]:")) else "collector_host_metrics_and_configured_http_probe",
    }
    store.add_sample(sample)
    return sample
