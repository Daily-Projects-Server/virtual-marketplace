# Remote imports
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.exceptions import TokenError
from django.conf import settings

# Local imports
from listings.models import Category, Listing
from orders.models import Cart
from .models import Settings

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
        login_url, data={"email": user_fixture.email, "password": "password123"}
    )
    assert login_response.status_code == status.HTTP_200_OK
    access_token = login_response.data["access_token"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")


def logout(user_fixture, client):
    if user_fixture.is_authenticated:
        logout_url = reverse("logout")
        client.post(logout_url)
        client.credentials()
