import pytest

from conftest import User
from listings.models import Category, Listing
from orders.models import Cart, CartItem


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
def listing_fixture(request, user_fixture):
    listing = Listing.objects.create(
        title="Test Listing",
        image="/test.jpg",
        description="Test Description",
        price=100.00,
        category=Category.objects.create(name="test", description="test"),
        quantity=10,
        owner_id=user_fixture.id,
    )
    request.addfinalizer(listing.delete)
    return listing


@pytest.fixture()
def cart_fixture(user_fixture):
    return Cart.objects.get(buyer=user_fixture)


@pytest.fixture()
def cart_item_fixture(request, cart_fixture, listing_fixture):
    cart_item = CartItem.objects.create(
        quantity=1, cart=cart_fixture, listing=listing_fixture
    )
    request.addfinalizer(cart_item.delete)
    return cart_item
