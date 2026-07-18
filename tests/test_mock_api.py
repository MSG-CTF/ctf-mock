import pytest

from mock_api.state import reset_mock_state


@pytest.fixture(autouse=True)
def reset_state():
    reset_mock_state()


def test_health_returns_django_status(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["service"] == "ctf-django"
    assert response.json()["database"] == "healthy"
    assert response.json()["cache"] == "healthy"


def test_scenario_can_make_django_database_unhealthy(client):
    scenario_response = client.post(
        "/api/scenarios",
        {"scenario": "django_db_down", "enabled": True},
        content_type="application/json",
    )
    health_response = client.get("/health")

    assert scenario_response.status_code == 200
    assert health_response.status_code == 503
    assert health_response.json()["status"] == "unhealthy"
    assert health_response.json()["database"] == "unhealthy"
    assert health_response.json()["reason"] == "database_unavailable"


def test_api_status_exposes_core_ctf_api_checks(client):
    response = client.get("/api/status")
    body = response.json()

    assert response.status_code == 200
    assert body["status"] == "healthy"
    assert {api["name"] for api in body["apis"]} == {
        "login",
        "scoreboard",
        "challenge",
        "submission",
    }


def test_instances_endpoint_returns_sentinel_targets(client):
    response = client.get("/api/instances")
    instances = response.json()

    assert response.status_code == 200
    assert instances[0]["instanceId"] == "inst-001"
    assert instances[0]["teamId"] == "team-001"
    assert instances[0]["challengeId"] == "web-basic-001"
    assert instances[0]["status"] == "running"
    assert instances[0]["healthUrl"].endswith("/api/instances/inst-001/health")


def test_instance_health_changes_by_scenario(client):
    client.post(
        "/api/scenarios",
        {"scenario": "instance_unhealthy", "enabled": True},
        content_type="application/json",
    )
    response = client.get("/api/instances/inst-001/health")

    assert response.status_code == 503
    assert response.json()["status"] == "unhealthy"
    assert response.json()["reason"] == "service_unavailable"


def test_broker_accounts_reflect_quota_scenario(client):
    client.post(
        "/api/scenarios",
        {"scenario": "quota_exhausted", "enabled": True},
        content_type="application/json",
    )
    response = client.get("/api/broker/accounts")
    account = response.json()[0]

    assert response.status_code == 200
    assert account["status"] == "quota_exhausted"
    assert account["quota"]["cpuUsed"] == account["quota"]["cpuLimit"]


def test_scheduler_signal_receiver_accepts_payload(client):
    response = client.post(
        "/api/scheduler/signals",
        {
            "type": "UNHEALTHY_INSTANCE",
            "severity": "warning",
            "target": "instance",
            "instanceId": "inst-001",
            "teamId": "team-001",
            "challengeId": "web-basic-001",
            "reason": "health_check_failed",
            "recommendedAction": "restart",
        },
        content_type="application/json",
    )

    assert response.status_code == 202
    assert response.json()["accepted"] is True
    assert response.json()["signalId"].startswith("sig-")


def test_admin_alert_receiver_accepts_payload(client):
    response = client.post(
        "/api/admin/alerts",
        {
            "severity": "critical",
            "target": "django",
            "reason": "django_db_unavailable",
            "message": "Django database is unavailable.",
            "recommendedAction": "manual_review",
        },
        content_type="application/json",
    )

    assert response.status_code == 202
    assert response.json()["accepted"] is True
    assert response.json()["alertId"].startswith("alert-")


@pytest.mark.parametrize(
    "scenario",
    [
        "django_down",
        "django_db_down",
        "django_cache_down",
        "django_api_timeout",
        "instance_unhealthy",
        "instance_timeout",
        "ttl_expired",
        "idle_timeout",
        "quota_exhausted",
        "budget_risk",
        "provider_failure",
        "broker_unavailable",
    ],
)
def test_required_scenarios_are_supported(client, scenario):
    response = client.post(
        "/api/scenarios",
        {"scenario": scenario, "enabled": True},
        content_type="application/json",
    )

    assert response.status_code == 200
    assert scenario in response.json()["activeScenarios"]


def test_unsupported_scenario_returns_bad_request(client):
    response = client.post(
        "/api/scenarios",
        {"scenario": "unknown_scenario", "enabled": True},
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "unsupported scenario"
