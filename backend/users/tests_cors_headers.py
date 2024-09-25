# Remote imports
import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework.test import APIClient


class TestCORSHeaders:
    @pytest.fixture(autouse=True)
    def setup_method(self, request):
        self.client = APIClient()

    @pytest.mark.django_db
    def test_cors_headers(self):
        url = reverse("login")
        response = self.client.options(url, HTTP_ORIGIN="http://localhost:3000")

        assert response["Access-Control-Allow-Origin"] == "http://localhost:3000"
        assert "POST" in response["Access-Control-Allow-Methods"]
        assert "authorization" in response["Access-Control-Allow-Headers"].lower()

    @pytest.mark.django_db
    def test_cors_allowed_origins(self):
        url = reverse("login")
        for origin in settings.CORS_ALLOWED_ORIGINS:
            response = self.client.options(url, HTTP_ORIGIN=origin)
            assert response["Access-Control-Allow-Origin"] == origin

    @pytest.mark.django_db
    def test_cors_disallowed_origin(self):
        url = reverse("login")
        disallowed_origin = "http://example.com"
        response = self.client.options(url, HTTP_ORIGIN=disallowed_origin)

        assert "Access-Control-Allow-Origin" not in response

    def test_cors_settings(self):
        assert "corsheaders" in settings.INSTALLED_APPS
        assert "corsheaders.middleware.CorsMiddleware" in settings.MIDDLEWARE
        assert hasattr(settings, "CORS_ALLOWED_ORIGINS")
        assert isinstance(settings.CORS_ALLOWED_ORIGINS, list)
        assert len(settings.CORS_ALLOWED_ORIGINS) > 0
