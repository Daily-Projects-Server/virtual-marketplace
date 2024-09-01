import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from listings.models import Listing, Category
from users.models import User


@pytest.fixture
def user(db):
    return User.objects.create_user(email="owner@example.com", password="password123")

@pytest.fixture
def another_user(db):
    return User.objects.create_user(email="nonowner@example.com", password="password456")

@pytest.fixture
def category(db):
    return Category.objects.create(name="Test Category", description="Test Description")

#Model tests
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
    assert listing.owner_id == owner.id
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

# Fixture and Endpoint Tests
@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def listing(db, user, category):
    return Listing.objects.create(
        owner=user,
        title="Original Title",
        description="Original Description",
        price=100.00,
        category=category
    )


@pytest.mark.django_db
def test_update_listing(client, user, listing):
    client.login(email="owner@example.com", password="password123")
    url = reverse('listing-detail', kwargs={'pk': listing.id})
    data = {
        "title": "Updated Title",
        "description": "Updated Description",
        "price": 150.00
    }
    response = client.patch(url, data)
    listing.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert listing.title == "Updated Title"
    assert listing.description == "Updated Description"
    assert listing.price == 150.00

@pytest.mark.django_db
def test_update_listing_non_owner(client, another_user, listing):
    client.login(email="nonowner@example.com", password="password456")
    url = reverse('listing-detail', kwargs={'pk': listing.id})
    data = {
        "title": "Attempted Update Title"
    }
    response = client.patch(url, data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
