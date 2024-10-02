import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from conftest import User
from listings.models import Category, Listing
from orders.models import Cart, CartItem


# Test the CartItem model
class TestCartItem:
    @pytest.mark.django_db
    def test_cart_item_model(self, listing_fixture, cart_fixture):
        cart_item = CartItem.objects.create(
            quantity=1, cart=cart_fixture, listing=listing_fixture
        )
        assert CartItem.objects.count() == 1
        assert cart_fixture == cart_item.cart
        assert listing_fixture == cart_item.listing
        assert cart_item.quantity == 1


# Test the Cart model and its endpoints
class TestCart:
    @pytest.mark.django_db
    def test_cart_model(self, user_fixture):
        assert Cart.objects.count() == 1

    @pytest.mark.django_db
    def test_get_cart_items(self, user_fixture, cart_fixture, listing_fixture):
        client = APIClient()
        client.force_authenticate(user_fixture)

        # Create a cart item
        CartItem.objects.create(quantity=1, cart=cart_fixture, listing=listing_fixture)

        # List
        cart_item_url = reverse("cart-item-list")
        response = client.get(cart_item_url)
        assert response.status_code == 200
        assert len(response.data) == 1

        # Retrieve
        cart_item = CartItem.objects.get(cart=cart_fixture, listing=listing_fixture)
        cart_item_url = reverse("cart-item-detail", args=[cart_item.id])
        response = client.get(cart_item_url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_add_item_to_cart(self, user_fixture, cart_fixture):
        client = APIClient()

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

        # Add the listing to the cart
        cart_item_url = reverse("cart-item-list")
        data = {"cart": cart_fixture.id, "listing": listing.id, "quantity": 1}
        response = client.post(
            cart_item_url,
            data,
        )
        assert response.status_code == 400

        # Try to add the same item to the cart
        client.force_authenticate(user_fixture)
        response = client.post(
            cart_item_url,
            data,
        )
        assert response.status_code == 201
        assert CartItem.objects.filter(cart=cart_fixture, listing=listing).exists()

        # Try to add the same item to the cart
        client.logout()
        response = client.post(
            cart_item_url,
            data,
        )
        assert response.status_code == 401

    @pytest.mark.django_db
    def test_remove_item_from_cart(self, user_fixture, cart_fixture, listing_fixture):
        client = APIClient()
        client.force_authenticate(user_fixture)

        # Add the listing to the cart
        cart_item_url = reverse("cart-item-list")
        response = client.post(
            cart_item_url,
            {
                "cart": cart_fixture.id,
                "listing": listing_fixture.id,
                "quantity": 1,
            },
        )
        assert response.status_code == 201

        # Remove the listing from the cart
        cart_item = CartItem.objects.get(cart=cart_fixture, listing=listing_fixture)
        cart_item_url = reverse("cart-item-detail", args=[cart_item.id])
        response = client.delete(cart_item_url)
        assert response.status_code == 204

    @pytest.mark.django_db
    def test_update_cart_item(self, user_fixture, cart_fixture, listing_fixture):
        client = APIClient()
        client.force_authenticate(user_fixture)

        # Add the listing to the cart
        cart_item_url = reverse("cart-item-list")
        response = client.post(
            cart_item_url,
            {
                "cart": cart_fixture.id,
                "listing": listing_fixture.id,
                "quantity": 1,
            },
        )

        # Retrieve the cart item
        cart_item = CartItem.objects.get(cart=cart_fixture, listing=listing_fixture)
        cart_item_url = reverse("cart-item-detail", args=[cart_item.id])

        # Update the quantity of the cart item
        data = client.get(cart_item_url).data
        data["quantity"] = 2
        response = client.put(cart_item_url, data)
        assert response.status_code == 200
        assert CartItem.objects.get(id=cart_item.id).quantity == 2

        # Try to update the quantity to a value greater than the available quantity
        data["quantity"] = 11
        response = client.put(cart_item_url, data)
        assert response.status_code == 400

        # Try to update the quantity to a value less than 1
        data["quantity"] = 0
        response = client.put(cart_item_url, data)
        assert response.status_code == 400
