from django.urls import path

from mock_api import views


urlpatterns = [
    path("health", views.health),
]
