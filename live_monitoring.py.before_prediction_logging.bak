
from __future__ import annotations

import json
import time
from typing import Any
from urllib.parse import urlparse

import numpy as np
import pandas as pd
import requests
import streamlit as st

from agents import IncidentAgents
from collectors.system_metrics import (
    DEFAULT_SERVICE_URL,
    BEARER_TOKEN,
    collect_live_sample,
    validate_local_service_url,
    validate_monitoring_target_url,
)
from approval import ApprovalStore, ApprovalError
from dl.anomaly_detector import FEATURES, SEQUENCE_LENGTH
from dl.live_training import (
    LIVE_MODEL_PATH,
    load_live_detector,
    train_live_model,
)
from storage.telemetry_store import TelemetryStore


MIN_TRAINING_SAMPLES = 180
LOOPBACK_HOSTS = {"localhost", "127.0.0.1", "::1"}
REQUEST_TIMEOUT = 2.0


def _is_loopback_target(service_url: str) -> bool:
    """Return True only when the URL hostname is a loopback address."""
    try:
        parsed = urlparse(service_url)
        return (
            parsed.scheme == "http"
            and (parsed.hostname or "").lower() in LOOPBACK_HOSTS
        )
    except (TypeError, ValueError):
        return False


def _get_service_health(service_url: str) -> dict[str, Any] | None:
    """Read the service health endpoint without following redirects."""
    try:
        headers = (
            {"Authorization": f"Bearer {BEARER_TOKEN}"}
            if BEARER_TOKEN
            else {}
        )
        response = requests.get(
            f"{service_url.rstrip('/')}/health",
            timeout=REQUEST_TIMEOUT,
            headers=headers,
            allow_redirects=False,
        )
        response.raise_for_status()

        body = response.json()
        if not isinstance(body, dict):
            return None

        return body

    except (requests.RequestException, ValueError):
        return None


def _bootstrap_analysis(sample: dict[str, Any]) -> dict[str, Any]:
    """Use explicit safety thresholds until a live model is available."""
    metrics = {
        name: float(sample[name])
        for name in FEATURES
    }

    rules = {
        "cpu_pct": (
            metrics["cpu_pct"] >= 90,
            "CPU at or above 90%",
        ),
        "memory_pct": (
            metrics["memory_pct"] >= 95,
            "Memory at or above 95%",
        ),
        "latency_ms": (
            metrics["latency_ms"] >= 1000,
            "Probe latency at or above 1000 ms",
        ),
        "error_rate_pct": (
            metrics["error_rate_pct"] > 0
            or int(sample.get("status_code", 0)) != 200,
            "Probe errors or non-200 response",
        ),
        "disk_pct": (
            metrics["disk_pct"] >= 95,
            "Disk usage at or above 95%",
        ),
    }

    flagged = [
        {
            "feature": feature,
            "reconstruction_error": None,
            "threshold": None,
            "reason": reason,
        }
        for feature, (triggered, reason) in rules.items()
        if triggered
    ]

    unavailable = not bool(sample.get("service_available", False))
    status_code = int(sample.get("status_code", 0))
    is_anomaly = bool(flagged or unavailable)

    if unavailable or status_code >= 500:
        severity = "HIGH"
    elif is_anomaly:
        severity = "MEDIUM"
    else:
        severity = "NORMAL"

    return {
        "is_anomaly": is_anomaly,
        "score": None,
        "threshold": None,
        "severity": severity,
        "flagged_features": flagged,
        "feature_errors": {},
        "latest_metrics": metrics,
        "model": "Bootstrap rules (live DL model unavailable)",
        "data_source": "Host metrics and HTTP probe; rule-based fallback",
    }


def _analyze_latest(
    store: TelemetryStore,
    samples: list[dict[str, Any]],
) -> tuple[dict[str, Any], str]:
    latest = samples[-1]

    if LIVE_MODEL_PATH.exists() and len(samples) >= SEQUENCE_LENGTH:
        try:
            detector = load_live_detector()
            window_rows = samples[-SEQUENCE_LENGTH:]

            window = np.asarray(
                [
                    [float(row[feature]) for feature in FEATURES]
                    for row in window_rows
                ],
                dtype=np.float32,
            )

            analysis = detector.detect(window)
            analysis["data_source"] = (
                "Live host metrics and HTTP probe telemetry"
            )

            guard_reasons: list[str] = []
            status_code = int(latest.get("status_code", 0))

            if status_code != 200:
                guard_reasons.append(
                    f"HTTP probe status {status_code}"
                )

            if float(latest.get("latency_ms", 0)) >= 1000:
                guard_reasons.append(
                    f"Probe latency {float(latest['latency_ms']):.1f} ms"
                )

            if float(latest.get("cpu_pct", 0)) >= 90:
                guard_reasons.append(
                    f"CPU {float(latest['cpu_pct']):.1f}%"
                )

            if float(latest.get("memory_pct", 0)) >= 95:
                guard_reasons.append(
                    f"Memory {float(latest['memory_pct']):.1f}%"
                )

            if float(latest.get("disk_pct", 0)) >= 95:
                guard_reasons.append(
                    f"Disk {float(latest['disk_pct']):.1f}%"
                )

            analysis["model_anomaly"] = bool(
                analysis.get("is_anomaly", False)
            )
            analysis["live_guard_triggered"] = bool(guard_reasons)
            analysis["live_guard_reasons"] = guard_reasons

            analysis["is_anomaly"] = bool(
                analysis.get("is_anomaly", False)
                or guard_reasons
                or not latest.get("service_available", False)
            )

            if (
                analysis["is_anomaly"]
                and analysis.get("severity") == "NORMAL"
            ):
                analysis["severity"] = (
                    "HIGH"
                    if status_code >= 500
                    or not latest.get("service_available", False)
                    else "MEDIUM"
                )

            mode = "live_lstm_autoencoder"

            store.annotate_sample(
                int(latest["id"]),
                analysis.get("score"),
                analysis["is_anomaly"],
                mode,
            )

            return analysis, mode

        except (
            ValueError,
            KeyError,
            RuntimeError,
            OSError,
            TypeError,
        ) as exc:
            st.warning(
                "The live DL model could not analyze this window. "
                f"Using rule-based fallback. Details: {exc}"
            )

    analysis = _bootstrap_analysis(latest)

    store.annotate_sample(
        int(latest["id"]),
        None,
        analysis["is_anomaly"],
        "bootstrap_rules",
    )

    return analysis, "bootstrap_rules"


def _service_logs(service_url: str) -> list[str]:
    """Fetch diagnostic logs without following redirects."""
    try:
        response = requests.get(
            f"{service_url.rstrip('/')}/logs?limit=12",
            timeout=REQUEST_TIMEOUT,
            allow_redirects=False,
        )
        response.raise_for_status()

        body = response.json()
        if not isinstance(body, dict):
            return ["The service returned an invalid logs response."]

        items = body.get("items", [])
        if not isinstance(items, list):
            return ["The service returned an invalid logs collection."]

        return [
            (
                f"{item.get('timestamp')} "
                f"status={item.get('status_code')} "
                f"latency_ms={item.get('latency_ms')} "
                f"fault_mode={item.get('fault_mode')}"
            )
            for item in items
            if isinstance(item, dict)
        ]

    except (
        requests.RequestException,
        ValueError,
        AttributeError,
    ):
        return [
            "Could not retrieve logs from the monitoring target."
        ]


def _build_live_incident(
    sample: dict[str, Any],
    analysis: dict[str, Any],
    service_url: str,
) -> dict[str, Any]:
    faults: list[str] = []

    status_code = int(sample.get("status_code", 0))
    latency_ms = float(sample.get("latency_ms", 0))

    if status_code != 200:
        faults.append(
            f"Latest HTTP probe returned status {status_code}"
        )

    if latency_ms >= 1000:
        faults.append(
            f"Probe latency reached {latency_ms:.1f} ms"
        )

    if float(sample.get("cpu_pct", 0)) >= 90:
        faults.append(
            f"Host CPU utilization reached "
            f"{float(sample['cpu_pct']):.1f}%"
        )

    if float(sample.get("memory_pct", 0)) >= 95:
        faults.append(
            f"Host memory utilization reached "
            f"{float(sample['memory_pct']):.1f}%"
        )

    if float(sample.get("disk_pct", 0)) >= 95:
        faults.append(
            f"Host disk utilization reached "
            f"{float(sample['disk_pct']):.1f}%"
        )

    if not faults:
        faults.append(
            "Live telemetry window exceeded its anomaly threshold"
        )

    description = (
        "Live AegisOps monitoring detected: "
        + "; ".join(faults)
    )

    logs = _service_logs(service_url)
    logs.extend(
        [
            (
                f"Live metrics: CPU={sample.get('cpu_pct')}%, "
                f"memory={sample.get('memory_pct')}%, "
                f"disk={sample.get('disk_pct')}%"
            ),
            (
                f"HTTP probe: status={status_code}, "
                f"latency_ms={latency_ms}, "
                f"error_rate_pct={sample.get('error_rate_pct')}"
            ),
            (
                f"Detector: {analysis.get('model')}; "
                f"anomaly={analysis.get('is_anomaly')}; "
                f"score={analysis.get('score')}; "
                f"threshold={analysis.get('threshold')}"
            ),
        ]
    )

    health = (
        _get_service_health(service_url)
        if _is_loopback_target(service_url)
        else None
    )

    can_clear_demo_fault = bool(
        health
        and health.get("status") == "ok"
        and health.get("fault_mode") in {"latency", "error"}
    )

    return {
        "id": f"LIVE-{int(sample['id']):06d}",
        "title": "Live telemetry anomaly",
        "category": (
            "API"
            if status_code != 200 or latency_ms >= 1000
            else "SERVER"
        ),
        "description": description,
        "logs": logs,
        "environment": (
            f"Monitored service {service_url}; "
            "host metrics refer to the collector machine"
        ),
        "root_cause": "To be determined from observed live evidence",
        "valid_actions": (
            ["clear_demo_service_fault"]
            if can_clear_demo_fault
            else ["capture_read_only_diagnostics"]
        ),
        "verification": (
            "For the local demo service, verify health and probe responses "
            "after an explicitly approved reset. Otherwise, collect "
            "read-only diagnostics."
        ),
    }


def _inject_fault(
    service_url: str,
    mode: str,
) -> dict[str, Any]:
    """Inject a test fault only into the validated local demo service."""
    if mode not in {"latency", "error"}:
        raise ValueError(
            "Fault injection only supports latency or error modes."
        )

    service_url = validate_local_service_url(service_url)

    response = requests.post(
        f"{service_url.rstrip('/')}/admin/fault",
        json={"mode": mode, "delay_ms": 1200},
        timeout=REQUEST_TIMEOUT,
        allow_redirects=False,
    )
    response.raise_for_status()

    body = response.json()
    if not isinstance(body, dict):
        raise RuntimeError("Invalid response from the demo service.")

    return body


def _run_agent_investigation(
    sample: dict[str, Any],
    analysis: dict[str, Any],
    service_url: str,
    store: TelemetryStore,
) -> dict[str, Any]:
    incident = _build_live_incident(
        sample,
        analysis,
        service_url,
    )

    agents = IncidentAgents()

    manager = agents.manager_step(incident).output
    investigation = agents.investigation_step(
        incident,
        manager,
        analysis,
    ).output
    diagnosis = agents.diagnosis_step(
        incident,
        investigation,
        analysis,
    ).output

    trace = {
        "incident": incident,
        "agent_mode": agents.mode,
        "manager": manager,
        "investigation": investigation,
        "diagnosis": diagnosis,
        "analysis": analysis,
    }

    store.log_event("live_agent_investigation", trace)

    return trace


def _resolve_local_test_fault(
    trace: dict[str, Any],
    service_url: str,
    store: TelemetryStore,
) -> dict[str, Any]:
    """
    Reset only the project's local demo fault switch.

    The caller must consume a valid approval before invoking this function.
    """
    service_url = validate_local_service_url(service_url)

    if not _is_loopback_target(service_url):
        raise RuntimeError(
            "Recovery is prohibited for remote targets."
        )

    health_before = _get_service_health(service_url)

    if not health_before:
        raise RuntimeError(
            "The local test service is unreachable. No recovery attempted."
        )

    if health_before.get("status") != "ok":
        raise RuntimeError(
            "Unexpected service identity or health response. "
            "No recovery attempted."
        )

    if health_before.get("fault_mode") not in {"latency", "error"}:
        raise RuntimeError(
            "No injected demo fault is active. No recovery attempted."
        )

    incident = trace["incident"]
    agents = IncidentAgents()

    resolution = agents.resolution_step(
        incident,
        trace["diagnosis"],
        [],
    ).output

    # Enforce the single permitted demo action regardless of agent output.
    resolution = {
        **resolution,
        "action_id": "clear_demo_service_fault",
        "safety_scope": "localhost demo service only",
    }

    response = requests.post(
        f"{service_url.rstrip('/')}/admin/fault",
        json={"mode": "normal", "delay_ms": 1200},
        timeout=REQUEST_TIMEOUT,
        allow_redirects=False,
    )
    response.raise_for_status()

    health_after = _get_service_health(service_url)
    probe_ok = False
    probe_status = 0
    probe_latency_ms: float | None = None

    try:
        started = time.perf_counter()

        probe_response = requests.get(
            f"{service_url.rstrip('/')}/probe",
            timeout=REQUEST_TIMEOUT,
            allow_redirects=False,
        )

        probe_latency_ms = (
            time.perf_counter() - started
        ) * 1000

        probe_status = probe_response.status_code
        probe_ok = (
            probe_status == 200
            and probe_latency_ms < 1000
        )

    except requests.RequestException:
        probe_ok = False

    success = bool(
        health_after
        and health_after.get("status") == "ok"
        and health_after.get("fault_mode") == "normal"
        and probe_ok
    )

    action_result = {
        "success": success,
        "action_id": "clear_demo_service_fault",
        "message": (
            "Demo fault reset and verification passed."
            if success
            else "Reset was requested, but verification failed."
        ),
        "health": health_after,
        "probe_status": probe_status,
        "probe_latency_ms": (
            round(probe_latency_ms, 3)
            if probe_latency_ms is not None
            else None
        ),
        "execution_scope": "Local AegisOps demo service only",
    }

    verification = agents.verification_step(
        incident,
        trace["diagnosis"],
        "clear_demo_service_fault",
        action_result,
    ).output

    outcome = {
        "resolution": resolution,
        "action_result": action_result,
        "verification": verification,
    }

    store.log_event(
        "live_local_remediation",
        {
            "incident_id": incident["id"],
            **outcome,
        },
    )

    return outcome


def render_live_monitoring() -> None:
    st.title("📡 Live Monitoring & Agent Investigation")

    st.caption(
        "Live host metrics, HTTP probe telemetry, optional LSTM detection, "
        "multi-agent investigation, and an approval-gated local demo "
        "recovery workflow."
    )

    store = TelemetryStore()

    url_value = st.text_input(
        "Monitoring target base URL",
        value=DEFAULT_SERVICE_URL,
        help=(
            "Remote targets must use HTTPS. Remote monitoring is read-only. "
            "Recovery is restricted to the validated local demo service."
        ),
    )

    try:
        service_url = validate_monitoring_target_url(url_value)
    except ValueError as exc:
        st.error(str(exc))
        return

    st.markdown("### 1. Live telemetry collector")

    st.write(
        "CPU, memory, and disk metrics describe this collector machine. "
        "HTTP latency and status describe the configured monitoring target."
    )

    @st.fragment(run_every="5s")
    def live_panel() -> None:
        # Define this before any conditional use.
        is_local_target = _is_loopback_target(service_url)
        service_health = _get_service_health(service_url)

        if service_health is None:
            st.warning(
                "The service health endpoint is unavailable. "
                "Start the local demo service if you are testing locally."
            )
            st.code(
                "python -m uvicorn demo_service.main:app "
                "--host 127.0.0.1 --port 8765",
                language="powershell",
            )
        else:
            st.success(
                f"Service reachable · status={service_health.get('status')} "
                f"· fault_mode={service_health.get('fault_mode', 'unknown')}"
            )

        collecting = st.checkbox(
            "Collect live metrics every 5 seconds",
            value=True,
            key="aegisops_live_collect",
        )

        if collecting:
            try:
                collect_live_sample(store, service_url)
            except (ValueError, OSError, RuntimeError) as exc:
                st.error(f"Collector error: {exc}")

        if st.button(
            "Collect one sample now",
            key="aegisops_manual_sample",
        ):
            try:
                collect_live_sample(store, service_url)
                st.toast("Live telemetry sample stored.")
            except Exception as exc:
                st.error(f"Collection failed: {exc}")

        rows = store.recent_samples(limit=1000)
        st.metric("Stored samples", store.sample_count())

        if not rows:
            st.info("Waiting for the first telemetry sample...")
            return

        latest = rows[-1]
        analysis, mode = _analyze_latest(store, rows)

        latest["anomaly_score"] = analysis.get("score")
        latest["is_anomaly"] = int(
            bool(analysis.get("is_anomaly"))
        )
        latest["detector_mode"] = mode

        metrics = st.columns(5)
        metrics[0].metric("CPU", f"{latest['cpu_pct']:.1f}%")
        metrics[1].metric("Memory", f"{latest['memory_pct']:.1f}%")
        metrics[2].metric("Disk", f"{latest['disk_pct']:.1f}%")
        metrics[3].metric(
            "Probe latency",
            f"{latest['latency_ms']:.1f} ms",
        )
        metrics[4].metric(
            "Probe HTTP",
            str(latest["status_code"]),
        )

        if analysis["is_anomaly"]:
            st.error(
                f"LIVE ANOMALY · severity {analysis['severity']} "
                f"· detector: {analysis['model']}"
            )

            if analysis.get("live_guard_reasons"):
                st.write(
                    "**Operational guardrails:** "
                    + "; ".join(analysis["live_guard_reasons"])
                )
        else:
            st.success(
                "No anomaly flagged in the latest window · "
                f"detector: {analysis['model']}"
            )

        previous_alert = bool(
            st.session_state.get(
                "aegisops_previous_live_alert",
                False,
            )
        )
        current_alert = bool(analysis["is_anomaly"])

        if current_alert and not previous_alert:
            alert_payload = {
                "sample_id": latest.get("id"),
                "sample": latest,
                "analysis": analysis,
            }
            store.log_event(
                "live_anomaly_detected",
                alert_payload,
            )
            st.session_state[
                "aegisops_current_live_incident"
            ] = alert_payload

        elif previous_alert and not current_alert:
            store.log_event(
                "live_anomaly_recovered",
                {
                    "sample_id": latest.get("id"),
                    "sample": latest,
                },
            )

        st.session_state[
            "aegisops_previous_live_alert"
        ] = current_alert

        if mode == "live_lstm_autoencoder":
            score_cols = st.columns(3)
            score_cols[0].metric(
                "LSTM reconstruction score",
                f"{analysis['score']:.5f}",
            )
            score_cols[1].metric(
                "Calibrated threshold",
                f"{analysis['threshold']:.5f}",
            )
            score_cols[2].metric(
                "Flagged features",
                len(analysis.get("flagged_features", [])),
            )
        else:
            st.info(
                "The live-data LSTM is not currently available. "
                "Detection is using explicit bootstrap rules."
            )

        chart = pd.DataFrame(rows[-240:])
        chart["timestamp"] = pd.to_datetime(
            chart["timestamp"],
            errors="coerce",
        )
        chart = chart.set_index("timestamp")

        left, right = st.columns(2)

        with left:
            st.write("**Host resource metrics (%)**")
            st.line_chart(
                chart[["cpu_pct", "memory_pct", "disk_pct"]],
                height=240,
            )

        with right:
            st.write("**HTTP probe measurements**")
            st.line_chart(
                chart[["latency_ms", "error_rate_pct"]],
                height=240,
            )

        st.write("**Latest telemetry samples**")

        visible_cols = [
            "timestamp",
            "cpu_pct",
            "memory_pct",
            "disk_pct",
            "latency_ms",
            "error_rate_pct",
            "status_code",
            "fault_mode",
            "anomaly_score",
            "is_anomaly",
        ]

        available_cols = [
            column
            for column in visible_cols
            if column in pd.DataFrame(rows).columns
        ]

        st.dataframe(
            pd.DataFrame(rows[-30:])[available_cols].iloc[::-1],
            hide_index=True,
            width="stretch",
        )

        if st.button(
            "Prepare CSV export from all stored samples",
            key="aegisops_prepare_csv",
        ):
            all_rows = store.all_samples()
            st.session_state["aegisops_live_csv_export"] = (
                pd.DataFrame(all_rows)
                .to_csv(index=False)
                .encode("utf-8")
            )
            st.success(
                f"Prepared {len(all_rows)} stored samples for export."
            )

        csv_export = st.session_state.get(
            "aegisops_live_csv_export"
        )

        if csv_export:
            st.download_button(
                "Download full telemetry CSV",
                data=csv_export,
                file_name="aegisops_live_telemetry.csv",
                mime="text/csv",
                key="aegisops_export_live_csv",
            )

        healthy = store.healthy_training_samples()

        st.markdown("### 2. Train the live LSTM")

        st.write(
            f"Healthy samples available: **{len(healthy)}**. "
            f"Training requires at least {MIN_TRAINING_SAMPLES} samples. "
            "This baseline is not proof of production-grade accuracy."
        )

        if st.button(
            "Train / retrain LSTM from healthy telemetry",
            disabled=len(healthy) < MIN_TRAINING_SAMPLES,
            key="aegisops_train_live",
        ):
            try:
                with st.spinner("Training the live telemetry model..."):
                    result = train_live_model(
                        healthy,
                        epochs=12,
                        min_samples=MIN_TRAINING_SAMPLES,
                    )

                store.log_event("live_model_trained", result)

                st.success(
                    f"Model trained. Threshold={result['threshold']:.5f}; "
                    f"training windows={result['training_windows']}; "
                    f"validation windows={result['validation_windows']}."
                )
                st.json(result)
                st.rerun()

            except (ValueError, RuntimeError, OSError) as exc:
                st.error(f"Training failed: {exc}")

        if LIVE_MODEL_PATH.exists():
            try:
                metadata_path = LIVE_MODEL_PATH.with_suffix(".json")
                metadata = json.loads(
                    metadata_path.read_text(encoding="utf-8")
                )
                st.caption(
                    f"Active model: {LIVE_MODEL_PATH.name} · "
                    f"training samples={metadata.get('training_samples', '?')}"
                )
            except (OSError, json.JSONDecodeError):
                st.caption(
                    f"Live checkpoint found: {LIVE_MODEL_PATH}"
                )

        st.markdown("### 3. Controlled fault lab")

        if not is_local_target:
            st.info(
                "Fault injection is disabled for remote monitoring targets."
            )
        else:
            st.write(
                "These controls affect the local demo service only. "
                "Fault injection is a test action, not a recovery action."
            )

            fault_cols = st.columns(2)

            with fault_cols[0]:
                if st.button(
                    "Inject 1.2 s latency",
                    key="aegisops_fault_latency",
                    disabled=service_health is None,
                ):
                    try:
                        _inject_fault(service_url, "latency")
                        store.log_event(
                            "test_fault_injected",
                            {
                                "mode": "latency",
                                "service_url": service_url,
                            },
                        )
                        st.success(
                            "Latency fault injected. Wait for new samples."
                        )
                    except Exception as exc:
                        st.error(f"Fault injection failed: {exc}")

            with fault_cols[1]:
                if st.button(
                    "Inject HTTP 500",
                    key="aegisops_fault_error",
                    disabled=service_health is None,
                ):
                    try:
                        _inject_fault(service_url, "error")
                        store.log_event(
                            "test_fault_injected",
                            {
                                "mode": "error",
                                "service_url": service_url,
                            },
                        )
                        st.success(
                            "HTTP 500 fault injected. Wait for new samples."
                        )
                    except Exception as exc:
                        st.error(f"Fault injection failed: {exc}")

        st.markdown(
            "### 4. Multi-agent investigation and approved recovery"
        )

        active = (
            bool(analysis.get("is_anomaly"))
            or not bool(latest.get("service_available"))
        )

        investigate = st.button(
            "Run agents on latest live evidence",
            type="primary",
            key="aegisops_live_investigate",
            disabled=not active,
        )

        if investigate:
            try:
                with st.spinner(
                    "Manager, Investigation, and Diagnosis agents are "
                    "analyzing the live evidence..."
                ):
                    trace = _run_agent_investigation(
                        latest,
                        analysis,
                        service_url,
                        store,
                    )

                st.session_state["aegisops_live_trace"] = trace
                st.success(
                    f"Investigation completed using {trace['agent_mode']}."
                )

            except Exception as exc:
                st.error(f"Agent investigation failed: {exc}")

        trace = st.session_state.get("aegisops_live_trace")

        if trace:
            with st.expander(
                "Live agent investigation trace",
                expanded=True,
            ):
                st.json(
                    {
                        key: trace[key]
                        for key in (
                            "agent_mode",
                            "manager",
                            "investigation",
                            "diagnosis",
                        )
                    }
                )

            st.write(
                f"**Incident:** {trace['incident']['id']} — "
                f"{trace['incident']['description']}"
            )

            current_health = (
                _get_service_health(service_url)
                if is_local_target
                else None
            )

            is_injected_fault = bool(
                is_local_target
                and current_health
                and current_health.get("status") == "ok"
                and current_health.get("fault_mode") in {"latency", "error"}
            )

            st.warning(
                "Recovery is restricted to clearing an injected fault "
                "on the local demo service. Remote targets are read-only."
            )
            st.caption(
                "Each recovery requires a one-time approval tied to "
                "the incident, action, and exact target."
            )

            approval_store = ApprovalStore(store.db_path)

            scope = {
                "action_id": "clear_demo_service_fault",
                "target": service_url,
                "incident_id": trace["incident"]["id"],
            }

            if st.button(
                "Request recovery approval",
                key="aegisops_request_recovery",
                disabled=not is_injected_fault,
            ):
                try:
                    ticket = approval_store.request(
                        **scope,
                        requested_by="local_operator",
                    )

                    st.session_state[
                        "aegisops_recovery_ticket"
                    ] = ticket["ticket_id"]

                    store.log_event(
                        "recovery_approval_requested",
                        {
                            key: ticket.get(key)
                            for key in (
                                "ticket_id",
                                "action_id",
                                "target",
                                "incident_id",
                                "expires_at",
                            )
                        },
                    )

                    st.rerun()

                except (ApprovalError, ValueError, RuntimeError) as exc:
                    st.error(f"Could not request approval: {exc}")

            ticket_id = st.session_state.get(
                "aegisops_recovery_ticket"
            )
            ticket = None

            if ticket_id:
                try:
                    ticket = approval_store.get(ticket_id)
                    st.write(
                        f"Approval ticket: `{ticket['ticket_id']}` · "
                        f"status: **{ticket['status']}** · "
                        f"expires: {ticket['expires_at']} UTC"
                    )
                except ApprovalError as exc:
                    st.error(str(exc))

            if ticket and ticket["status"] == "pending":
               
                
                approver_label = st.text_input(
                "Approver label (audit note only; not authenticated)",
                placeholder="Example: local_operator",
                help=(
                    "Enter a short label using letters, numbers, "
                    "underscores, or hyphens. This does not verify identity."
                ),
                max_chars=40,
                key="aegisops_approver_label_v2",
            )


                phrase = st.text_input(
                    "Type exactly: APPROVE clear_demo_service_fault",
                    key="aegisops_approval_phrase",
                )
                valid_approver_label = (
    approver_label.strip() != ""
    and all(
        char.isalnum() or char in "_-"
        for char in approver_label.strip()
    )
)
                if st.button(
                    "Approve this recovery action",
                    key="aegisops_approve_recovery",
                    disabled=(
                         not is_injected_fault
    or not valid_approver_label
                    ),
                ):
                    try:
                        approved = approval_store.approve(
                            ticket_id,
                            **scope,
                            approved_by=approver_label.strip(),
                            confirmation=phrase,
                        )

                        store.log_event(
                            "recovery_approval_granted",
                            {
                                "ticket_id": ticket_id,
                                "approved_by": approved["approved_by"],
                                **scope,
                            },
                        )

                        st.success(
                            "Approval recorded. Recheck the target "
                            "before executing recovery."
                        )
                        st.rerun()

                    except (ApprovalError, ValueError) as exc:
                        st.error(f"Approval rejected: {exc}")

            if ticket and ticket["status"] == "approved":
                st.warning(
                    "This approval is one-time and expires. "
                    "Execution consumes it before the recovery attempt."
                )

                if st.button(
                    "Execute approved recovery and verify",
                    key="aegisops_live_resolve",
                    disabled=not is_injected_fault,
                ):
                    try:
                        # Consume first to prevent replay.
                        approval_store.consume(
                            ticket_id,
                            **scope,
                        )

                        store.log_event(
                            "recovery_approval_consumed",
                            {
                                "ticket_id": ticket_id,
                                **scope,
                            },
                        )

                        with st.spinner(
                            "Running the local recovery and checking "
                            "the resulting health and probe responses..."
                        ):
                            outcome = _resolve_local_test_fault(
                                trace,
                                service_url,
                                store,
                            )

                        st.session_state[
                            "aegisops_live_resolution"
                        ] = outcome

                        store.log_event(
                            "recovery_execution_finished",
                            {
                                "ticket_id": ticket_id,
                                "success": bool(
                                    outcome["action_result"]["success"]
                                ),
                                **scope,
                            },
                        )

                        if outcome["action_result"]["success"]:
                            st.success(
                                "Local demo fault cleared and verified."
                            )
                        else:
                            st.error(
                                "Recovery was attempted, but verification "
                                "did not pass."
                            )

                        st.rerun()

                    except Exception as exc:
                        store.log_event(
                            "recovery_execution_failed",
                            {
                                "ticket_id": ticket_id,
                                "error": str(exc),
                                **scope,
                            },
                        )
                        st.error(f"Recovery was not completed: {exc}")

            if ticket and ticket["status"] in {
                "consumed",
                "rejected",
                "expired",
            }:
                if st.button(
                    "Clear completed approval ticket",
                    key="aegisops_clear_ticket",
                ):
                    st.session_state.pop(
                        "aegisops_recovery_ticket",
                        None,
                    )
                    st.rerun()

            resolution = st.session_state.get(
                "aegisops_live_resolution"
            )
            if resolution:
                st.json(resolution)

        st.markdown("### 5. Incident and model audit trail")

        events = store.recent_events(limit=20)

        if events:
            audit_df = pd.DataFrame(
                [
                    {
                        "timestamp": event["timestamp"],
                        "event_type": event["event_type"],
                        "details": json.dumps(
                            event["payload"],
                            default=str,
                        )[:500],
                    }
                    for event in events
                ]
            )

            st.dataframe(
                audit_df,
                hide_index=True,
                width="stretch",
            )
        else:
            st.caption(
                "No incident events have been recorded yet."
            )

    live_panel()
