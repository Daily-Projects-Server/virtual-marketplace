# Remore imports
import io
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

# Local imports
from listings.models import Category, Listing
from conftest import User


@pytest.fixture()
def owner_fixture(request):
    user = User.objects.create_user(
        email="TEST@EXAMPLE.COM",
        password="password123",
        first_name="John",
        last_name="Doe",
    )
    request.addfinalizer(user.delete)
    return user


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
def listing_fixture(request, owner_fixture, category_fixture):
    listing = Listing(
        title="Test Listing",
        image="listing_images/test.jpg",
        description="Test Description",
        price=100.00,
        quantity=10,
        owner_id=owner_fixture.id,
        category=category_fixture,
    )
    listing.save()
    request.addfinalizer(listing.delete)
    return listing
