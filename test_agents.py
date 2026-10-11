from agents import IncidentAgents
from simulator import get_incidents, execute_action
from dl.anomaly_detector import generate_incident_telemetry, load_detector


def test_local_agents_work_without_api_key(monkeypatch):
    monkeypatch.setattr("agents.GROQ_API_KEY", "")
    agents = IncidentAgents()
    incident = next(x for x in get_incidents() if x["id"] == "INC-1001")
    detector = load_detector()
    telemetry, _ = generate_incident_telemetry(incident["id"])
    dl_result = detector.detect(telemetry)

    manager = agents.manager_step(incident).output
    investigation = agents.investigation_step(incident, manager, dl_result).output
    diagnosis = agents.diagnosis_step(incident, investigation, dl_result).output
    resolution = agents.resolution_step(incident, diagnosis).output
    assert agents.mode.startswith("Offline")
    assert dl_result["is_anomaly"]
    assert investigation["deep_learning_analysis"]["is_anomaly"] is True
    assert diagnosis["root_cause"]
    assert resolution["action_id"] in incident["valid_actions"]


def test_local_verification_uses_simulator_result(monkeypatch):
    monkeypatch.setattr("agents.GROQ_API_KEY", "")
    agents = IncidentAgents()
    incident = get_incidents()[0]
    verification = agents.verification_step(incident, {}, "restart_connection_pool", {"success": True})
    assert verification.output["verified"] is True
    assert verification.output["next_step"] == "close_incident"


def test_simulator_contract_still_works():
    incident = get_incidents()[0]
    action = next(a for a, ok in incident["effects"].items() if ok)
    assert execute_action(incident, action)["success"] is True
    assert execute_action(incident, action, force_fail=True)["success"] is False
