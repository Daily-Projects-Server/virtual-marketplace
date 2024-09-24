import pytest
from pytest_django.fixtures import client

from listings.models import Listing, Category
from users.models import User
from orders.models import Cart, CartItem
from users.tests import login

from rest_framework.test import APIClient


class TestCartItem:
    @pytest.fixture()
    def test_user(self, request):
        user = User.objects.create_user(
            email="TEST@EXAMPLE.COM",
            password="password123",
            first_name="John",
            last_name="Doe",
        )
        request.addfinalizer(user.delete)
        return user

    @pytest.fixture()
    def test_listing(self, request, test_user):
        listing = Listing.objects.create(
            title="Test Listing",
            image="/test.jpg",
            description="Test Description",
            price=100.00,
            category=Category.objects.create(name="test", description="test"),
            quantity=10,
            owner_id=test_user.id,
        )
        request.addfinalizer(listing.delete)
        return listing

    @pytest.fixture()
    def test_cart(self, test_user):
        return Cart.objects.get(buyer=test_user)

    @pytest.mark.django_db
    def test_cart_item_model(self, test_user, test_listing, test_cart):
        cart_item = CartItem.objects.create(quantity=1)
        cart_item.cart.set([test_cart])
        cart_item.listing.set([test_listing])
        assert CartItem.objects.count() == 1
        assert test_cart in cart_item.cart.all()
        assert test_listing in cart_item.listing.all()
        assert cart_item.quantity == 1


class TestCart:
    @pytest.fixture()
    def test_user(self, request):
        user = User.objects.create_user(
            email="TEST@EXAMPLE.COM",
            password="password123",
            first_name="John",
            last_name="Doe",
        )
        request.addfinalizer(user.delete)
        return user

    @pytest.fixture()
    def test_listing(self, request, test_user):
        listing = Listing.objects.create(
            title="Test Listing",
            image="/test.jpg",
            description="Test Description",
            price=100.00,
            category=Category.objects.create(name="test", description="test"),
            quantity=10,
            owner_id=test_user.id,
        )
        request.addfinalizer(listing.delete)
        return listing

    @pytest.fixture()
    def test_cart(self, test_user):
        return Cart.objects.get(buyer=test_user)

    @pytest.mark.django_db
    def test_cart_model(self, test_user):
        assert Cart.objects.count() == 1

    @pytest.mark.django_db
    def test_add_item_to_cart(self, test_user, test_cart):
        # Login as test user
        client = APIClient()
        login(test_user, client)
        assert client.get("/users/").status_code == 200

        # Create a listing from another user to add to the cart
        user = User.objects.create_user(
            email="newtest@test.com", password="password123"
        )
        listing = Listing.objects.create(
            title="Test Listing",
            image="/test.jpg",
            description="Test Description",
            price=100.00,
            category=Category.objects.create(name="test", description="test"),
            quantity=10,
            owner_id=user.id,
        )

        # Change the listing to a cart item
        response = client.post(
            "/cart-item/", {"cart": test_cart.id, "listing": listing.id, "quantity": 1}
        )
        assert response.status_code == 201
