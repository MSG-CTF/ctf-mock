from rest_framework import status as http_status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from mock_api import state


@api_view(["GET"])
def health(request):
    payload = state.django_health()
    response_status = http_status.HTTP_200_OK

    if payload["status"] != "healthy":
        response_status = http_status.HTTP_503_SERVICE_UNAVAILABLE

    return Response(payload, status=response_status)


@api_view(["GET"])
def api_status(request):
    return Response(state.django_api_status())


@api_view(["GET"])
def instances(request):
    base_url = request.build_absolute_uri("/").rstrip("/")
    return Response(state.monitored_instances(base_url))


@api_view(["GET"])
def instance_health(request, instance_id):
    payload = state.instance_health(instance_id)

    if payload is None:
        return Response(
            {"detail": "instance not found"},
            status=http_status.HTTP_404_NOT_FOUND,
        )

    if payload["status"] == "timeout":
        return Response(payload, status=http_status.HTTP_504_GATEWAY_TIMEOUT)

    if payload["status"] != "healthy":
        return Response(payload, status=http_status.HTTP_503_SERVICE_UNAVAILABLE)

    return Response(payload)


@api_view(["GET"])
def broker_accounts(request):
    payload = state.broker_accounts()

    if payload[0]["status"] == "broker_unavailable":
        return Response(payload, status=http_status.HTTP_503_SERVICE_UNAVAILABLE)

    return Response(payload)


@api_view(["POST"])
def scheduler_signals(request):
    signal = state.record_scheduler_signal(request.data)
    return Response(
        {
            "accepted": True,
            "signalId": signal["signalId"],
            "receivedAt": signal["receivedAt"],
        },
        status=http_status.HTTP_202_ACCEPTED,
    )


@api_view(["POST"])
def admin_alerts(request):
    alert = state.record_admin_alert(request.data)
    return Response(
        {
            "accepted": True,
            "alertId": alert["alertId"],
            "receivedAt": alert["receivedAt"],
        },
        status=http_status.HTTP_202_ACCEPTED,
    )


@api_view(["POST"])
def scenarios(request):
    scenario = request.data.get("scenario")
    enabled = request.data.get("enabled", True)

    if not state.is_supported_scenario(scenario):
        return Response(
            {
                "detail": "unsupported scenario",
                "supportedScenarios": sorted(state.SUPPORTED_SCENARIOS),
            },
            status=http_status.HTTP_400_BAD_REQUEST,
        )

    state.apply_scenario(scenario, enabled)

    return Response(
        {
            "scenario": scenario,
            "enabled": enabled,
            "activeScenarios": state.active_scenarios(),
        }
    )
