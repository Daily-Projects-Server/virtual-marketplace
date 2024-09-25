import pytest
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.exceptions import TokenError
from django.conf import settings

from listings.models import Listing, Category
from orders.models import Cart
from .models import Settings


User = get_user_model()

# Authentication
def login(test_user, client):
    login_url = reverse('login')
    login_response = client.post(login_url, data={"email": test_user.email, "password": "password123"})
    assert login_response.status_code == status.HTTP_200_OK
    access_token = login_response.data["access_token"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

def logout(test_user, client):
    if test_user.is_authenticated:
        logout_url = reverse('logout')
        client.post(logout_url)
        client.credentials()

class TestUserModel:
    @pytest.fixture()
    def test_user(self, request):
        user = User.objects.create_user(email="TEST@EXAMPLE.COM", password="password123", first_name="John",
                                        last_name="Doe")
        request.addfinalizer(user.delete)
        return user

    @pytest.fixture()
    def test_superuser(self, request):
        superuser = User.objects.create_superuser(email="admin@example.com", password="admin123", first_name="Admin",
                                                  last_name="User")
        request.addfinalizer(superuser.delete)
        return superuser

    @pytest.mark.django_db
    def test_create_user_with_valid_data(self, test_user):
        assert test_user.email == "test@example.com"
        assert test_user.check_password("password123")
        assert test_user.first_name == "John"
        assert test_user.last_name == "Doe"
        assert test_user.settings is not None

    @pytest.mark.django_db
    def test_create_user_without_email_raises_error(self):
        with pytest.raises(ValueError, match="The Email field must be set"):
            User.objects.create_user(email="", password="password123")

    @pytest.mark.django_db
    def test_create_user_without_password_raises_error(self):
        with pytest.raises(ValueError, match="The Password field must be set"):
            User.objects.create_user(email="test@example.com", password="")

    @pytest.mark.django_db
    def test_create_superuser_with_valid_data(self, test_superuser):
        assert test_superuser.is_staff
        assert test_superuser.is_superuser

    @pytest.mark.django_db
    def test_create_superuser_without_is_staff_raises_error(self):
        with pytest.raises(ValueError, match="Superuser must have is_staff=True."):
            User.objects.create_superuser(email="admin@example.com", password="admin123", is_staff=False)

    @pytest.mark.django_db
    def test_create_superuser_without_is_superuser_raises_error(self):
        with pytest.raises(ValueError, match="Superuser must have is_superuser=True."):
            User.objects.create_superuser(email="admin@example.com", password="admin123", is_superuser=False)

    @pytest.mark.django_db
    def test_user_has_perm_returns_true_for_superuser(self, test_superuser):
        assert test_superuser.has_perm("any_perm")

    @pytest.mark.django_db
    def test_user_has_perms_returns_true_for_superuser(self, test_superuser):
        assert test_superuser.has_perms(["perm1", "perm2"])

    @pytest.mark.django_db
    def test_user_email_is_lowercase_on_save(self, test_user):
        assert test_user.email == "test@example.com"

    @pytest.mark.django_db
    def test_user_has_default_settings(self, test_user):
        assert test_user.settings is not None
        assert test_user.settings.dark_mode is False

    @pytest.mark.django_db
    def test_total_number_of_settings_instances_are_one_when_all_users_have_default_settings(self):
        User.objects.create_user(email='user1@example.com', password='password1', first_name='John', last_name='Doe'),
        User.objects.create_user(email='user2@example.com', password='password2', first_name='Jane', last_name='Smith'),
        User.objects.create_user(email='user3@example.com', password='password3', first_name='Jim', last_name='Beam'),
        settings = Settings.objects.all()
        assert settings.count() == 1

    @pytest.mark.django_db
    def test_if_settings_instance_is_created_when_user_change_settings(self, test_user):
        test_user.settings.dark_mode = True
        test_user.save()
        assert Settings.objects.count() == 2
        assert test_user.settings.id == 2
        assert Settings.objects.get(id=1).dark_mode is False
        assert Settings.objects.get(id=2).dark_mode is True
        assert test_user.settings.dark_mode is True

    @pytest.mark.django_db
    def test_if_settings_instance_is_not_deleted_when_user_is_deleted(self, test_user):
        test_user = User.objects.create_user(email="test@test.com", password="password123")
        test_user.delete()
        assert Settings.objects.count() == 1

    @pytest.mark.django_db
    def test_if_cart_is_created_when_user_is_created(self, test_user):
        assert test_user.cart is not None
        assert test_user.cart.buyer == test_user
        assert test_user.cart.cartitem_set.count() == 0
        assert Cart.objects.count() == 1


class TestUserViews:
    @pytest.fixture()
    def test_user(self, request):
        user = User.objects.create_user(email="test@test.com", password="password123")
        request.addfinalizer(user.delete)
        return user

    @pytest.mark.django_db
    def test_user_can_register(self, test_user):
        client = APIClient()
        register_url = reverse('register')

        response = client.post(register_url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        data = {
            "first_name": "test",
            "last_name": "name",
            "password": "arandompassword@4320",
            "confirm_password": "arandompassword@4320",
            "email": "test@email.com",
        }
        response = client.post(register_url, data=data)
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.django_db
    def test_user_can_login(self, test_user):
        client = APIClient()
        login_url = reverse('login')

        response = client.post(login_url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        data = {
            "email": test_user.email,
            "password": "password123",
        }
        response = client.post(login_url, data=data)
        assert response.status_code == status.HTTP_200_OK

        data["password"] = "wrong-password"
        response = client.post(login_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_user_can_logout(self, test_user):
        client = APIClient()
        login_url = reverse('login')
        logout_url = reverse('logout')

        response = client.post(logout_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = client.post(login_url, data={"email": test_user.email, "password": "password123"})
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access_token']}")
        assert response.status_code == status.HTTP_200_OK

        response = client.post(logout_url)
        assert response.status_code == status.HTTP_200_OK

        with pytest.raises(TokenError):
            response = client.post(logout_url)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED




class TestReviewViews:
    @pytest.fixture()
    def test_user(self, request):
        user = User.objects.create_user(email="test@example.com", password="password123", first_name="John",
                                        last_name="Doe")
        request.addfinalizer(user.delete)
        return user

    @pytest.fixture()
    def test_listing(self, request):
        owner = User.objects.create_user(email="test", password="test")
        listing = Listing.objects.create(
            title="Test Listing",
            image="listing_images/test.jpg",
            description="Test Description",
            price=100.00,
            quantity=10,
            owner_id=owner.id,
            category=Category.objects.create(name="Test Category")
        )
        request.addfinalizer(listing.delete)
        request.addfinalizer(owner.delete)
        return listing


    @pytest.mark.django_db
    def test_create_review(self, test_user, test_listing):
        client = APIClient()
        review_url = reverse('review-list')

        # Review with valid data
        review_data = {
            "user": test_user.id,
            "listing": test_listing.id,
            "rating": 3,
            "comment": "Test Review"
        }

        # Try to post a review without authentication
        assert client.post(review_url, data=review_data).status_code == status.HTTP_401_UNAUTHORIZED

        # Authenticate the user
        login(test_user, client)

        # Post a review with valid data
        response = client.post(review_url, data=review_data)
        assert response.status_code == status.HTTP_201_CREATED

        review_data["rating"] = 6
        response = client.post(review_url, data=review_data)

        # Try to post a review with invalid data
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Try to post a review on own listing
        listing = Listing.objects.create(
            title="Test Listing",
            image="listing_images/test.jpg",
            description="Test Description",
            price=100.00,
            quantity=10,
            owner_id=test_user.id,
            category=Category.objects.create(name="Test Category")
        )
        # Update the review data to post a review on the listing
        review_data["listing"] = listing.id
        review_data["rating"] = 3

        response = client.post(review_url, data=review_data)

        # Check if the response is 403 Forbidden
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_retrieve_reviews(self, test_user, test_listing):
        client = APIClient()
        review_url = reverse('review-list')

        # List reviews
        response = client.get(review_url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_update_review(self, test_user, test_listing):
        client = APIClient()

        # Authenticate the user
        login(test_user, client)

        # Create a review
        review_url = reverse('review-list')
        review_data = {
            "user": test_user.id,
            "listing": test_listing.id,
            "rating": 3,
            "comment": "Test Review"
        }
        response = client.post(review_url, data=review_data)

        # Update the review
        review = response.data
        review_data["rating"] = 5
        response = client.put(f'{review_url}{review["id"]}/', data=review_data)
        assert response.status_code == status.HTTP_200_OK

        # Update the review with invalid data
        review_data["rating"] = 6
        response = client.put(f'{review_url}{review["id"]}/', data=review_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Update the review on own listing
        review_data["user"] = 1
        response = client.put(f'{review_url}{review["id"]}/', data=review_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Update the review without authentication
        logout(test_user, client)
        response = client.put(f'{review_url}{review["id"]}/', data=review_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    @pytest.mark.django_db
    def test_destroy_review(self, test_user, test_listing):
        client = APIClient()

        # Create user
        user = User.objects.create_user(email="second@second.com", password="password123")

        # Authenticate the user
        login(user, client)

        # Create a review
        review_url = reverse('review-list')
        review_data = {
            "user": user.id,
            "listing": test_listing.id,
            "rating": 3,
            "comment": "Test Review"
        }
        response = client.post(review_url, data=review_data)

        # Delete the review
        review = response.data
        response = client.delete(f'{review_url}{review["id"]}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Delete the review without authentication
        logout(user, client)
        response = client.delete(f'{review_url}{review["id"]}/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Delete the review on own listing with different user
        login(test_user, client)
        review_data["user"] = Listing.objects.get(id=review["listing"]).owner_id
        response = client.post(review_url, data=review_data)
        review = response.data
        response = client.delete(f'{review_url}{review["id"]}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

class TestCORSHeaders:
    @pytest.fixture(autouse=True)
    def setup_method(self, request):
        self.client = APIClient()

    @pytest.mark.django_db
    def test_cors_headers(self):
        url = reverse('login')
        response = self.client.options(url, HTTP_ORIGIN='http://localhost:3000')

        assert response['Access-Control-Allow-Origin'] == 'http://localhost:3000'
        assert 'POST' in response['Access-Control-Allow-Methods']
        assert 'authorization' in response['Access-Control-Allow-Headers'].lower()

    @pytest.mark.django_db
    def test_cors_allowed_origins(self):
        url = reverse('login')
        for origin in settings.CORS_ALLOWED_ORIGINS:
            response = self.client.options(url, HTTP_ORIGIN=origin)
            assert response['Access-Control-Allow-Origin'] == origin

    @pytest.mark.django_db
    def test_cors_disallowed_origin(self):
        url = reverse('login')
        disallowed_origin = 'http://example.com'
        response = self.client.options(url, HTTP_ORIGIN=disallowed_origin)
        
        assert 'Access-Control-Allow-Origin' not in response

    def test_cors_settings(self):
        assert 'corsheaders' in settings.INSTALLED_APPS
        assert 'corsheaders.middleware.CorsMiddleware' in settings.MIDDLEWARE
        assert hasattr(settings, 'CORS_ALLOWED_ORIGINS')
        assert isinstance(settings.CORS_ALLOWED_ORIGINS, list)
        assert len(settings.CORS_ALLOWED_ORIGINS) > 0