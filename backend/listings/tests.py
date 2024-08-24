import pytest

from users.models import User
from rest_framework.exceptions import ValidationError

from listings.models import Listing, Category


class TestListingsModels:
    @pytest.fixture()
    def owner(self):
        return User.objects.create_user(email="testl@email.com", password="password123")

    @pytest.fixture()
    def category(self):
        return Category.objects.create(name="Test Category", description="Test Description")

    @pytest.mark.django_db
    def test_listing_model(self, owner, category):
        listing = Listing(
            title="Test Listing",
            image="listing_images/test.jpg",
            description="Test Description",
            price=100.00,
            quantity=10,
            owner_id=owner.id,
            category=category
        )
        listing.save()

        assert listing.title == "Test Listing"
        assert listing.image == "listing_images/test.jpg"
        assert listing.description == "Test Description"
        assert listing.price == 100.00
        assert listing.quantity == 10
        assert listing.owner_id == 1
        assert listing.category.name == "Test Category"
        assert listing.category.description == "Test Description"

    @pytest.mark.django_db
    def test_listing_clean(self, owner, category):
        listing = Listing(
            title="Test Listing",
            image="listing_images/test.jpg",
            description="Test Description",
            price=-100.00,
            quantity=-10,
            owner_id=owner.id,
            category=category
        )
        with pytest.raises(ValidationError) as e:
            listing.clean()
        listing.price = 100.00
        with pytest.raises(ValidationError) as e:
            listing.save()

    @pytest.mark.django_db
    def test_listing_save(self, owner, category):
        listing = Listing(
            title="Test Listing",
            image="listing_images/test.jpg",
            description="Test Description",
            price=100.00,
            quantity=0,
            owner_id=owner.id,
            category=category
        )
        listing.save()
        assert listing.active is False
        listing.quantity = 10
        listing.save()
        assert listing.active is True

    @pytest.mark.django_db
    def test_owner_having_multiple_listings(self, owner, category):
        listing1 = Listing(
            title="Test Listing 1",
            image="listing_images/test1.jpg",
            description="Test Description",
            price=100.00,
            quantity=10,
            owner_id=owner.id,
            category=category
        )
        listing1.save()
        listing2 = Listing(
            title="Test Listing 2",
            image="listing_images/test2.jpg",
            description="Test Description",
            price=100.00,
            quantity=10,
            owner_id=owner.id,
            category=category
        )
        listing2.save()
        assert Listing.objects.filter(owner_id=owner.id).count() == 2