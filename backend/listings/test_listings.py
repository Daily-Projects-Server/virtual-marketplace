# Remove imports
import io
import pytest
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from listings.models import Category, Listing
from users.models import User
from users.common_for_tests import login
from listings.models import Listing, Category


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


class TestListingsModel:
    @pytest.mark.django_db
    def test_listing_model(self, owner_fixture, category_fixture):
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

        # Test listing model fields
        assert listing.title == "Test Listing"
        assert listing.image == "listing_images/test.jpg"
        assert listing.description == "Test Description"
        assert listing.price == 100.00
        assert listing.quantity == 10
        assert listing.owner_id == 1
        assert listing.category.name == "Test Category"
        assert listing.category.description == "Test Description"

    @pytest.mark.django_db
    def test_listing_clean(self, listing_fixture):
        listing = listing_fixture

        # Test listing price and quantity validation
        listing.price = -100.00
        listing.quantity = -10
        with pytest.raises(ValidationError):
            listing.clean()
        listing.price = 100.00
        with pytest.raises(ValidationError):
            listing.save()

    @pytest.mark.django_db
    def test_listing_save(self, listing_fixture):
        listing = listing_fixture

        # Testt listing activity when quantity is 0
        listing.quantity = 0
        listing.save()
        assert listing.active is False

        # Test listing activity when quantity is greater than 0
        listing.quantity = 10
        listing.save()
        assert listing.active is True

    @pytest.mark.django_db
    def test_owner_having_multiple_listings(self, owner_fixture, category_fixture):
        # Listing 1
        listing1 = Listing(
            title="Test Listing 1",
            image="listing_images/test1.jpg",
            description="Test Description",
            price=100.00,
            quantity=10,
            owner_id=owner_fixture.id,
            category=category_fixture,
        )
        listing1.save()

        # Listing 2
        listing2 = Listing(
            title="Test Listing 2",
            image="listing_images/test2.jpg",
            description="Test Description",
            price=100.00,
            quantity=10,
            owner_id=owner_fixture.id,
            category=category_fixture,
        )
        listing2.save()
        assert Listing.objects.filter(owner_id=owner_fixture.id).count() == 2


class TestListingViews:
    @pytest.mark.django_db
    def test_listing_list_view(self, listing_fixture):
        client = APIClient()

        listing_url = reverse("listing-list")
        response = client.get(listing_url)
        assert response.status_code == 200
        assert len(response.data) == 1

    @pytest.mark.django_db
    def test_listing_detail_view(self, listing_fixture):
        client = APIClient()

        listing_url = reverse("listing-detail", args=[listing_fixture.id])
        response = client.get(listing_url)
        assert response.status_code == 200
        assert response.data["title"] == "Test Listing"

    @pytest.mark.django_db
    def test_listing_create_view(self, owner_fixture, category_fixture, image_fixture):
        client = APIClient()
        client.force_authenticate(user=owner_fixture)
        listing_url = reverse("listing-list")

        # Test creating a listing with valid data
        data = {
            "title": "Test Listing",
            "image": image_fixture,
            "description": "Test Description",
            "price": 100.00,
            "quantity": 10,
            "owner": owner_fixture.id,
            "category": category_fixture.id,
        }

        response = client.post(listing_url, data=data, format="multipart")
        assert response.status_code == 201
        assert response.data["title"] == "Test Listing"

        # Test creating a listing with invalid data
        data["price"] = -100.00
        response = client.post(listing_url, data=data, format="multipart")
        assert response.status_code == 400


    @pytest.mark.django_db
    def test_listing_update_view(self, owner_fixture, listing_fixture):
        client = APIClient()
        client.force_authenticate(user=owner_fixture)

        listing_url = reverse("listing-detail", args=[listing_fixture.id])
        data = {"title": "Updated Test Listing"}

        response = client.patch(listing_url, data=data)
        assert response.status_code == 200
        assert response.data["title"] == "Updated Test Listing"

        data = {"active": False}
        response = client.patch(listing_url, data=data)
        assert response.status_code == 200
        assert response.data["active"] == False
