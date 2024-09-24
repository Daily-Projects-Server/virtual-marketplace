import pytest
from pytest_django.fixtures import client

from listings.models import Listing, Category
from users.models import User
from orders.models import Cart, CartItem
from users.tests import login

from rest_framework.test import APIClient
from django.urls import reverse


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
        cart_item = CartItem.objects.create(
            quantity=1, cart=test_cart, listing=test_listing
        )
        assert CartItem.objects.count() == 1
        assert test_cart == cart_item.cart
        assert test_listing == cart_item.listing
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
        users_url = reverse("user-list")
        assert client.get(users_url).status_code == 200

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
        cart_item_url = reverse("cart-item-list")
        data = {"cart": test_cart.id, "listing": listing.id, "quantity": 1}
        response = client.post(
            cart_item_url,
            data,
        )
        assert response.status_code == 201

        # Try to add the same item to the cart
        response = client.post(
            cart_item_url,
            data,
        )
        assert response.status_code == 403


    @pytest.mark.django_db
    def test_remove_item_from_cart(self, test_user, test_cart, test_listing):
        client = APIClient()
        login(test_user, client)
        cart_item_url = reverse("cart-item-list")
        response = client.post(
            cart_item_url,
            {"cart": test_cart.id, "listing": test_listing.id, "quantity": 1},
        )
        assert response.status_code == 201

        cart_item = CartItem.objects.get(cart=test_cart, listing=test_listing)
        cart_item_url = reverse("cart-item-detail", args=[cart_item.id])
        response = client.delete(cart_item_url)
        assert response.status_code == 204


    @pytest.mark.django_db
    def test_update_cart_item(self, test_user, test_cart, test_listing):
        client = APIClient()
        CartItem.objects.create(
            quantity=1, cart=test_cart, listing=test_listing
        )
        login(test_user, client)

        cart_item = CartItem.objects.get(cart=test_cart, listing=test_listing)
        cart_item_url = reverse("cart-item-detail", args=[cart_item.id])
        data = client.get(cart_item_url).data
        data["quantity"] = 2
        response = client.put(cart_item_url, data)
        assert response.status_code == 200
        assert CartItem.objects.get(id=cart_item.id).quantity == 2
