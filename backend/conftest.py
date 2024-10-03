import io
import os

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from listings.models import Category, Listing
from orders.models import Cart

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


@pytest.fixture()
def category_fixture(request):
    category = Category.objects.create(
        name="Test Category", description="Test Description"
    )
    request.addfinalizer(category.delete)
    return category


@pytest.fixture()
def image_fixture(request):
    image = Image.new("RGB", (100, 100))
    image_file = io.BytesIO()
    image.save(image_file, format="JPEG")
    image_file.seek(0)
    image = SimpleUploadedFile(
        name="test_image.jpg", content=image_file.read(), content_type="image/jpeg"
    )

    request.addfinalizer(image.file.close)
    return image


@pytest.fixture()
def cart_fixture(user_fixture):
    return Cart.objects.get(buyer=user_fixture)


# Helper functions


def delete_image(image):
    if os.path.isfile(image.path):
        os.remove(image.path)
