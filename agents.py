import json
import re
from dataclasses import dataclass
from typing import Any

try:
    from groq import Groq
except ImportError:
    Groq = None

from config import GROQ_API_KEY, GROQ_MODEL


@dataclass
class AgentResult:
    agent: str
    output: dict[str, Any]


def _local_root_cause(text: str) -> str:
    value = text.lower()
    if any(k in value for k in ["pool exhausted", "connection pool", "database connection failed"]):
        return "Database connection pool exhausted, causing payment API requests to fail."
    if any(k in value for k in ["customer-db", "database unavailable", "service=stopped", "connection refused"]):
        return "The database service is stopped or refusing connections."
    if any(k in value for k in ["http 500", "status=500", "elevated response latency", "probe latency"]):
        return "The monitored local service is returning errors or responding slower than its healthy baseline."
    if any(k in value for k in ["cpu", "worker-service", "worker process"]):
        return "Worker processes are saturating CPU capacity."
    if any(k in value for k in ["disk", "no space left", "/var usage"]):
        return "The server disk volume is nearly full, preventing application writes."
    if any(k in value for k in ["oauth", "token validation", "auth-service"]):
        return "The OAuth configuration is inconsistent, causing token validation failures."
    if any(k in value for k in ["timeout", "service-a", "service-b", "route"]):
        return "The service-to-service network path or route is causing request timeouts."
    return "Insufficient evidence for a unique root cause; inspect service logs and dependencies."


def _preferred_actions(root_cause: str) -> list[str]:
    value = root_cause.lower()
    if "connection pool" in value:
        return ["restart_connection_pool", "increase_connection_pool", "restart_payment_service"]
    if "database service" in value or "database" in value:
        return ["restart_database_service", "clear_database_connection_pool", "restart_application_service"]
    if "cpu" in value or "worker" in value:
        return ["scale_worker_instances", "restart_worker_service", "restart_web_service"]
    if "disk" in value or "volume" in value:
        return ["rotate_application_logs", "restart_application_service", "restart_database_service"]
    if "oauth" in value or "token" in value:
        return ["restore_oauth_configuration", "restart_auth_service", "clear_login_cache"]
    if "network" in value or "route" in value or "timeout" in value:
        return ["refresh_service_route", "restart_service_b", "restart_service_a"]
    return []


class GroqAgent:
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        self.client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY and Groq is not None else None

    def run(self, payload: str) -> dict[str, Any]:
        if self.client is None:
            return self._run_local(json.loads(payload))
        response = self.client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": payload}
            ],
            temperature=0.1,
            max_tokens=1200,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content or "{}"
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", content, re.S)
            if not match:
                raise ValueError(f"{self.name} returned invalid JSON: {content}")
            return json.loads(match.group(0))

    def _run_local(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Deterministic offline agent behavior for demos and tests without an API key."""
        if self.name == "Manager Agent":
            category = payload.get("category", "GENERAL")
            return {
                "incident_category": category,
                "priority": "P1" if category in {"DATABASE", "API", "NETWORK"} else "P2",
                "investigation_tasks": [
                    "Review the supplied application and system logs",
                    "Inspect telemetry anomaly scores from the LSTM Autoencoder",
                    "Compare evidence against known service dependencies",
                ],
                "objective": "Identify a plausible root cause and select a safe, verifiable remediation.",
                "execution_mode": "offline_demo",
            }

        if self.name == "Investigation Agent":
            logs = payload.get("logs", [])
            telemetry = payload.get("deep_learning_analysis", {}) or {}
            flagged = telemetry.get("flagged_features", [])
            signals = [f"Log evidence: {line}" for line in logs[:4]]
            if telemetry.get("is_anomaly"):
                names = [x.get("feature", "unknown") for x in flagged]
                signals.append(
                    f"LSTM Autoencoder flagged abnormal telemetry; affected features: {', '.join(names) or 'overall sequence score'}"
                )
            else:
                signals.append("LSTM Autoencoder did not exceed its calibrated anomaly threshold.")
            root_cause = _local_root_cause(
                str(payload.get("incident", "")) + " " + " ".join(logs) + " " + str(payload.get("environment", ""))
            )
            return {
                "evidence": logs[:6],
                "signals": signals,
                "candidate_causes": [root_cause],
                "confidence": 0.82 if telemetry.get("is_anomaly") else 0.66,
                "deep_learning_analysis": telemetry,
                "execution_mode": "offline_demo",
            }

        if self.name == "Diagnosis Agent":
            investigation = payload.get("investigation", {}) or {}
            text = " ".join(investigation.get("evidence", [])) + " " + " ".join(investigation.get("signals", []))
            text += " " + str(payload.get("incident", ""))
            cause = _local_root_cause(text)
            return {
                "root_cause": cause,
                "evidence_used": investigation.get("evidence", [])[:4],
                "confidence": investigation.get("confidence", 0.65),
                "reasoning_summary": "The diagnosis matches the strongest log signals and uses DL telemetry as supporting evidence.",
                "execution_mode": "offline_demo",
            }

        if self.name == "Resolution Agent":
            diagnosis = payload.get("root_cause", {}) or {}
            if isinstance(diagnosis, dict):
                root_cause = str(diagnosis.get("root_cause", ""))
            else:
                root_cause = str(diagnosis)
            catalog = payload.get("action_catalog", [])
            catalog_ids = [item.get("action_id", "") for item in catalog]
            failed = set(payload.get("actions_already_tried", []))
            preferred = _preferred_actions(root_cause)
            action = next((a for a in preferred if a in catalog_ids and a not in failed), None)
            if action is None:
                action = next((a for a in catalog_ids if a not in failed), "")
            return {
                "action_id": action,
                "rationale": "Selected from the approved action catalog based on the diagnosed failure; previously failed actions are excluded.",
                "expected_result": "The affected service metric and incident verification condition return to a healthy state.",
                "execution_mode": "offline_demo",
            }

        if self.name == "Verification Agent":
            action_result = payload.get("simulated_action_result", {}) or {}
            verified = bool(action_result.get("success", False))
            return {
                "verified": verified,
                "verification_status": "PASS" if verified else "FAIL",
                "evidence": action_result.get("message", "No simulator result was provided."),
                "next_step": "close_incident" if verified else "retry_with_new_plan",
                "execution_mode": "offline_demo",
            }

        return {"status": "offline_demo", "message": f"No local handler for {self.name}."}


MANAGER_PROMPT = """
You are the Manager Agent in an IT incident resolution system.
Classify the incident, decide what evidence should be investigated, and define the investigation objective.
Return JSON with keys: incident_category, priority, investigation_tasks, objective.
"""

INVESTIGATOR_PROMPT = """
You are the Log and Telemetry Investigation Agent.
Analyze the incident description, logs, environment, manager plan, and the provided LSTM Autoencoder result.
Treat model output as evidence, not ground truth. Identify concrete evidence, suspicious signals, and candidate root causes.
Return JSON with keys: evidence, signals, candidate_causes, confidence.
"""

DIAGNOSIS_PROMPT = """
You are the Root Cause Agent.
Use only the provided incident evidence, investigation, and deep-learning telemetry analysis. Do not assume an anomaly alone proves causation.
Select the most likely root cause and explain the evidence briefly.
Return JSON with keys: root_cause, evidence_used, confidence, reasoning_summary.
Keep reasoning_summary concise and do not expose hidden chain-of-thought.
"""

RESOLUTION_PROMPT = """
You are the Resolution Agent.
Choose exactly ONE action_id from the provided action catalog that is most likely to resolve the incident.
Do not invent an action_id and do not repeat an action that has already failed.
Return JSON with keys: action_id, rationale, expected_result.
"""

VERIFICATION_PROMPT = """
You are the Verification Agent.
Determine whether the remediation actually resolved the incident.
Use the expected verification condition and the supplied action result. Do not mark a failed tool result as resolved.
Return JSON with keys: verified, verification_status, evidence, next_step.
next_step must be either "close_incident" or "retry_with_new_plan".
"""


class IncidentAgents:
    def __init__(self):
        self.manager = GroqAgent("Manager Agent", MANAGER_PROMPT)
        self.investigator = GroqAgent("Investigation Agent", INVESTIGATOR_PROMPT)
        self.diagnosis = GroqAgent("Diagnosis Agent", DIAGNOSIS_PROMPT)
        self.resolution = GroqAgent("Resolution Agent", RESOLUTION_PROMPT)
        self.verification = GroqAgent("Verification Agent", VERIFICATION_PROMPT)
        self.mode = "Groq LLM" if self.manager.client is not None else "Offline demo (no Groq API key)"

    def manager_step(self, incident):
        payload = json.dumps({
            "incident": incident["description"],
            "category": incident["category"],
            "environment": incident["environment"]
        }, indent=2)
        return AgentResult(self.manager.name, self.manager.run(payload))

    def investigation_step(self, incident, manager, deep_learning_analysis=None):
        payload = json.dumps({
            "incident": incident["description"],
            "logs": incident["logs"],
            "environment": incident["environment"],
            "manager_plan": manager,
            "deep_learning_analysis": deep_learning_analysis or {},
        }, indent=2)
        return AgentResult(self.investigator.name, self.investigator.run(payload))

    def diagnosis_step(self, incident, investigation, deep_learning_analysis=None):
        payload = json.dumps({
            "incident": incident["description"],
            "logs": incident["logs"],
            "investigation": investigation,
            "deep_learning_analysis": deep_learning_analysis or {},
        }, indent=2)
        return AgentResult(self.diagnosis.name, self.diagnosis.run(payload))

    def resolution_step(self, incident, diagnosis, failed_actions=None):
        failed_actions = failed_actions or []
        catalog = [
            {"action_id": a, "description": a.replace("_", " ")} for a in incident["valid_actions"]
        ]
        payload = json.dumps({
            "incident": incident["description"],
            "root_cause": diagnosis,
            "action_catalog": catalog,
            "actions_already_tried": failed_actions,
            "instruction": "Select the safest likely action from the catalog and do not repeat a failed action."
        }, indent=2)
        return AgentResult(self.resolution.name, self.resolution.run(payload))

    def verification_step(self, incident, diagnosis, action_id, action_result):
        payload = json.dumps({
            "incident": incident["description"],
            "root_cause": diagnosis,
            "verification_condition": incident["verification"],
            "selected_action": action_id,
            "simulated_action_result": action_result
        }, indent=2)
        return AgentResult(self.verification.name, self.verification.run(payload))
