from django.urls import path

from mock_api import views

urlpatterns = [
    path("health", views.health),
    path("api/status", views.api_status),
    path("api/instances", views.instances),
    path("api/instances/<str:instance_id>/health", views.instance_health),
    path("api/broker/accounts", views.broker_accounts),
    path("api/scheduler/signals", views.scheduler_signals),
    path("api/admin/alerts", views.admin_alerts),
    path("api/scenarios", views.scenarios),
]
