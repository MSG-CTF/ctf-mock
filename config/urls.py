from django.urls import include, path

urlpatterns = [
    path("", include("mock_api.urls")),
]
