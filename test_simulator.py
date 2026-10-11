from simulator import get_incidents, execute_action


def test_incidents_loaded():
    incidents = get_incidents()
    assert len(incidents) >= 5
    assert all("id" in x and "valid_actions" in x for x in incidents)


def test_known_action_resolves():
    incident = get_incidents()[0]
    action = next(a for a, ok in incident["effects"].items() if ok)
    result = execute_action(incident, action)
    assert result["success"] is True


def test_forced_failure():
    incident = get_incidents()[0]
    action = next(a for a, ok in incident["effects"].items() if ok)
    result = execute_action(incident, action, force_fail=True)
    assert result["success"] is False
