"""Independent telemetry collection process.

Run with: python -m collectors.worker
This process is intentionally read-only with respect to monitored targets.
"""
from __future__ import annotations

import logging
import os
import signal
import time

from collectors.system_metrics import DEFAULT_SERVICE_URL, REQUEST_TIMEOUT_S, collect_live_sample
from storage.telemetry_store import TelemetryStore

LOG_LEVEL = os.getenv("AEGISOPS_LOG_LEVEL", "INFO").upper()
INTERVAL = max(1.0, float(os.getenv("AEGISOPS_COLLECTION_INTERVAL_S", "5")))

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("aegisops.collector")
_running = True


def _stop(*_: object) -> None:
    global _running
    _running = False


def main() -> None:
    global _running
    signal.signal(signal.SIGINT, _stop)
    if hasattr(signal, "SIGTERM"):
        signal.signal(signal.SIGTERM, _stop)
    store = TelemetryStore()
    logger.info("Collector started target=%s interval=%ss", DEFAULT_SERVICE_URL, INTERVAL)
    while _running:
        started = time.monotonic()
        try:
            sample = collect_live_sample(store, DEFAULT_SERVICE_URL, REQUEST_TIMEOUT_S)
            logger.info(
                "sample id=%s status=%s latency_ms=%.2f error_rate_pct=%.2f",
                sample.get("id", "?"), sample["status_code"], sample["latency_ms"], sample["error_rate_pct"]
            )
        except Exception:
            logger.exception("Collection failed; continuing after interval")
        elapsed = time.monotonic() - started
        deadline_sleep = max(0.0, INTERVAL - elapsed)
        end = time.monotonic() + deadline_sleep
        while _running and time.monotonic() < end:
            time.sleep(min(0.25, end - time.monotonic()))
    logger.info("Collector stopped")


if __name__ == "__main__":
    main()
