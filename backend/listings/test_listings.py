import pytest
from rest_framework.exceptions import ValidationError

from listings.models import Category, Listing
from users.models import User


@pytest.fixture()
def owner_fixture(request):
    user = User.objects.create_user(email="testl@email.com", password="password123")
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
