from __future__ import annotations

import asyncio
import time
from collections import deque
from datetime import datetime, timezone
from threading import Lock
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="AegisOps Local Test Service", version="1.0.0")
_state_lock = Lock()
_fault_mode: Literal["normal", "latency", "error"] = "normal"
_delay_ms = 1200
_request_log: deque[dict] = deque(maxlen=500)


class FaultConfig(BaseModel):
    mode: Literal["normal", "latency", "error"] = "normal"
    delay_ms: int = Field(default=1200, ge=100, le=5000)


def _state() -> tuple[str, int]:
    with _state_lock:
        return _fault_mode, _delay_ms


def _log(path: str, status_code: int, elapsed_ms: float, fault_mode: str) -> None:
    _request_log.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "path": path,
        "status_code": status_code,
        "latency_ms": round(elapsed_ms, 3),
        "fault_mode": fault_mode,
    })


@app.get("/")
def root() -> dict:
    return {"service": "AegisOps local test service", "status": "running"}


@app.get("/health")
def health() -> dict:
    mode, _ = _state()
    return {"status": "ok", "service": "aegisops-demo-service", "fault_mode": mode}


@app.get("/probe")
async def probe() -> dict:
    start = time.perf_counter()
    mode, delay = _state()
    if mode == "latency":
        await asyncio.sleep(delay / 1000)
    elapsed = (time.perf_counter() - start) * 1000
    if mode == "error":
        _log("/probe", 500, elapsed, mode)
        raise HTTPException(status_code=500, detail="Injected local test fault: HTTP 500")
    _log("/probe", 200, elapsed, mode)
    return {"status": "ok", "fault_mode": mode, "server_processing_ms": round(elapsed, 3)}


@app.get("/logs")
def logs(limit: int = 50) -> dict:
    limit = min(max(limit, 1), 200)
    return {"items": list(_request_log)[-limit:]}


@app.post("/admin/fault")
def set_fault(config: FaultConfig) -> dict:
    """Local demo-only fault injection. Bind this app to 127.0.0.1, never a public interface."""
    global _fault_mode, _delay_ms
    with _state_lock:
        _fault_mode = config.mode
        _delay_ms = config.delay_ms
    return {"status": "ok", "fault_mode": _fault_mode, "delay_ms": _delay_ms}
