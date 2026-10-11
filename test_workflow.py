from agents import IncidentAgents
from dl.anomaly_detector import generate_incident_telemetry, load_detector
from simulator import execute_action, get_incidents


def run_local_workflow(incident, detector, force_first_failure=False):
    agents = IncidentAgents()
    window, _ = generate_incident_telemetry(incident["id"])
    dl_result = detector.detect(window)
    manager = agents.manager_step(incident).output
    investigation = agents.investigation_step(incident, manager, dl_result).output
    diagnosis = agents.diagnosis_step(incident, investigation, dl_result).output
    failed_actions = []
    steps = []

    for attempt in range(3):
        resolution = agents.resolution_step(incident, diagnosis, failed_actions).output
        action = resolution["action_id"]
        assert action in incident["valid_actions"]
        assert action not in failed_actions
        result = execute_action(
            incident,
            action,
            force_fail=bool(force_first_failure and attempt == 0),
        )
        verification = agents.verification_step(incident, diagnosis, action, result).output
        steps.append({"action": action, "success": result["success"], "verified": verification["verified"]})
        if result["success"]:
            return steps, dl_result, diagnosis
        failed_actions.append(action)
        investigation = agents.investigation_step(
            incident,
            {**manager, "previous_failure": result, "failed_actions": failed_actions},
            dl_result,
        ).output
        diagnosis = agents.diagnosis_step(
            incident,
            {**investigation, "previous_failure": result, "failed_actions": failed_actions},
            dl_result,
        ).output
    return steps, dl_result, diagnosis


def test_all_six_incidents_resolve_in_offline_demo_mode(monkeypatch):
    monkeypatch.setattr("agents.GROQ_API_KEY", "")
    detector = load_detector()
    for incident in get_incidents():
        steps, dl_result, diagnosis = run_local_workflow(incident, detector)
        assert dl_result["is_anomaly"], incident["id"]
        assert diagnosis["root_cause"]
        assert steps[-1]["success"], incident["id"]
        assert steps[-1]["verified"], incident["id"]


def test_payment_api_demo_shows_self_correction(monkeypatch):
    monkeypatch.setattr("agents.GROQ_API_KEY", "")
    detector = load_detector()
    incident = next(item for item in get_incidents() if item["id"] == "INC-1001")
    steps, _, _ = run_local_workflow(incident, detector, force_first_failure=True)
    assert len(steps) == 2
    assert steps[0]["success"] is False
    assert steps[1]["success"] is True
