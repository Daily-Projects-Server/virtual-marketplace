import os

import pytest
from django.conf import settings  # noqa: F401
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from listings.models import Category, Listing

os.environ["DJANGO_SETTINGS_MODULE"] = "api.settings"

User = get_user_model()


# Fixtures
@pytest.fixture()
def user_fixture(request):
    user = User.objects.create_user(
        email="TEST@EXAMPLE.COM",
        password="password123",
        first_name="John",
        last_name="Doe",
    )
    request.addfinalizer(user.delete)
    return user


@pytest.fixture()
def superuser_fixture(request):
    superuser = User.objects.create_superuser(
        email="admin@example.com",
        password="admin123",
        first_name="Admin",
        last_name="User",
    )
    request.addfinalizer(superuser.delete)
    return superuser


@pytest.fixture()
def listing_fixture(request):
    owner = User.objects.create_user(email="test", password="test")
    listing = Listing.objects.create(
        title="Test Listing",
        image="listing_images/test.jpg",
        description="Test Description",
        price=100.00,
        quantity=10,
        owner_id=owner.id,
        category=Category.objects.create(name="Test Category"),
    )
    request.addfinalizer(listing.delete)
    request.addfinalizer(owner.delete)
    return listing


# Authentication functions
def login(user_fixture, client):
    login_url = reverse("login")
    login_response = client.post(
        login_url,
        data={"email": user_fixture.email, "password": "password123"},
    )
    access_token = login_response.data["access_token"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")


def logout(user_fixture, client):
    if user_fixture.is_authenticated:
        logout_url = reverse("logout")
        client.post(logout_url)
        client.credentials()


def delete_image(image):
    if os.path.isfile(image.path):
        os.remove(image.path)
        