import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "incidents.json"

with open(DATA_FILE, "r", encoding="utf-8") as f:
    INCIDENTS = json.load(f)


def get_incidents():
    return INCIDENTS


def get_incident(incident_id):
    return next(x for x in INCIDENTS if x["id"] == incident_id)


def execute_action(incident, action_id, force_fail=False):
    effects = incident.get("effects", {})
    success = bool(effects.get(action_id, False)) and not force_fail
    if success:
        return {
            "success": True,
            "status": "RESOLVED",
            "message": f"Simulated action '{action_id}' completed successfully."
        }
    return {
        "success": False,
        "status": "NOT_RESOLVED",
        "message": f"Simulated action '{action_id}' completed, but verification conditions are still failing."
    }
