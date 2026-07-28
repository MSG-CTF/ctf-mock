from copy import deepcopy
from datetime import timedelta

from django.utils import timezone


SUPPORTED_SCENARIOS = {
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
}


_active_scenarios = set()
_received_signals = []
_received_alerts = []


def now_iso():
    return timezone.now().isoformat().replace("+00:00", "Z")


def reset_mock_state():
    _active_scenarios.clear()
    _received_signals.clear()
    _received_alerts.clear()


def apply_scenario(scenario, enabled):
    if scenario == "reset":
        reset_mock_state()
        return

    if enabled:
        _active_scenarios.add(scenario)
        return

    _active_scenarios.discard(scenario)


def is_supported_scenario(scenario):
    return scenario == "reset" or scenario in SUPPORTED_SCENARIOS


def active_scenarios():
    return sorted(_active_scenarios)


def django_health():
    if "django_down" in _active_scenarios:
        return {
            "status": "unhealthy",
            "service": "ctf-django",
            "database": "unknown",
            "cache": "unknown",
            "reason": "django_unavailable",
            "checkedAt": now_iso(),
        }

    if "django_db_down" in _active_scenarios:
        return {
            "status": "unhealthy",
            "service": "ctf-django",
            "database": "unhealthy",
            "cache": "healthy",
            "reason": "database_unavailable",
            "checkedAt": now_iso(),
        }

    if "django_cache_down" in _active_scenarios:
        return {
            "status": "unhealthy",
            "service": "ctf-django",
            "database": "healthy",
            "cache": "unhealthy",
            "reason": "cache_unavailable",
            "checkedAt": now_iso(),
        }

    return {
        "status": "healthy",
        "service": "ctf-django",
        "database": "healthy",
        "cache": "healthy",
        "checkedAt": now_iso(),
    }


def django_api_status():
    apis = [
        {"name": "login", "path": "/api/auth/login", "status": "healthy", "latencyMs": 80},
        {"name": "scoreboard", "path": "/api/scoreboard", "status": "healthy", "latencyMs": 120},
        {"name": "challenge", "path": "/api/challenges", "status": "healthy", "latencyMs": 90},
        {"name": "submission", "path": "/api/submissions", "status": "healthy", "latencyMs": 95},
    ]

    if "django_api_timeout" in _active_scenarios:
        # timeout을 실제 sleep으로 만들면 테스트가 느려져서 상태값으로만 표현한다.
        for api in apis:
            api["status"] = "timeout"
            api["latencyMs"] = 5000
        return {
            "status": "unhealthy",
            "reason": "django_api_timeout",
            "apis": apis,
            "checkedAt": now_iso(),
        }

    return {
        "status": "healthy",
        "apis": apis,
        "checkedAt": now_iso(),
    }


def monitored_instances(base_url):
    created_at = timezone.now() - timedelta(minutes=30)
    last_activity_at = timezone.now() - timedelta(minutes=5)
    status = "running"

    if "ttl_expired" in _active_scenarios:
        created_at = timezone.now() - timedelta(hours=2)

    if "idle_timeout" in _active_scenarios:
        last_activity_at = timezone.now() - timedelta(hours=1)

    if "instance_unhealthy" in _active_scenarios or "instance_timeout" in _active_scenarios:
        status = "unhealthy"

    return [
        {
            "instanceId": "inst-001",
            "teamId": "team-001",
            "challengeId": "web-basic-001",
            "status": status,
            "healthUrl": f"{base_url}/api/instances/inst-001/health",
            "createdAt": created_at.isoformat().replace("+00:00", "Z"),
            "lastActivityAt": last_activity_at.isoformat().replace("+00:00", "Z"),
            "ttlSeconds": 3600,
            "idleTimeoutSeconds": 900,
            "restartCount": 0,
        }
    ]


def instance_health(instance_id):
    if instance_id != "inst-001":
        return None

    if "instance_timeout" in _active_scenarios:
        return {
            "instanceId": instance_id,
            "status": "timeout",
            "reason": "health_check_timeout",
            "checkedAt": now_iso(),
        }

    if "instance_unhealthy" in _active_scenarios:
        return {
            "instanceId": instance_id,
            "status": "unhealthy",
            "reason": "service_unavailable",
            "checkedAt": now_iso(),
        }

    return {
        "instanceId": instance_id,
        "status": "healthy",
        "latencyMs": 50,
        "checkedAt": now_iso(),
    }


def broker_accounts():
    account = {
        "accountId": "acct-001",
        "provider": "aws",
        "status": "available",
        "quota": {
            "cpuUsed": 60,
            "cpuLimit": 100,
            "memoryUsedGb": 120,
            "memoryLimitGb": 256,
        },
        "budget": {
            "usedUsd": 80,
            "limitUsd": 100,
            "riskLevel": "normal",
        },
    }

    if "quota_exhausted" in _active_scenarios:
        account["status"] = "quota_exhausted"
        account["quota"]["cpuUsed"] = account["quota"]["cpuLimit"]
        return [account]

    if "budget_risk" in _active_scenarios:
        account["status"] = "budget_risk"
        account["budget"]["riskLevel"] = "warning"
        account["budget"]["usedUsd"] = 95
        return [account]

    if "provider_failure" in _active_scenarios:
        account["status"] = "provider_failure"
        account["reason"] = "cloud_adapter_failure"
        return [account]

    if "broker_unavailable" in _active_scenarios:
        account["status"] = "broker_unavailable"
        account["reason"] = "broker_status_unavailable"
        return [account]

    return [account]


def record_scheduler_signal(payload):
    signal_id = f"sig-{len(_received_signals) + 1:03d}"
    signal = deepcopy(payload)
    signal["signalId"] = signal_id
    signal["receivedAt"] = now_iso()
    _received_signals.append(signal)
    return signal


def record_admin_alert(payload):
    alert_id = f"alert-{len(_received_alerts) + 1:03d}"
    alert = deepcopy(payload)
    alert["alertId"] = alert_id
    alert["receivedAt"] = now_iso()
    _received_alerts.append(alert)
    return alert
