import pytest
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.exceptions import TokenError

from listings.models import Listing, Category
from .models import Settings

User = get_user_model()


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


class TestUserViews:
    @pytest.fixture()
    def test_user(self, request):
        user = User.objects.create_user(email="test@test.com", password="password123")
        request.addfinalizer(user.delete)
        return user

    @pytest.mark.django_db
    def test_user_can_register(self, test_user):
        client = APIClient()

        response = client.post('/register/')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        data = {
            "first_name": "test",
            "last_name": "name",
            "password": "arandompassword@4320",
            "confirm_password": "arandompassword@4320",
            "email": "test@email.com",
        }
        response = client.post("/register/", data=data)
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.django_db
    def test_user_can_login(self, test_user):
        client = APIClient()

        response = client.post('/login/')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        data = {
            "email": test_user.email,
            "password": "password123",
        }
        response = client.post('/login/', data=data)
        assert response.status_code == status.HTTP_200_OK

        data["password"] = "wrong-password"
        response = client.post('/login/', data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_user_can_logout(self, test_user):
        client = APIClient()

        response = client.post('/logout/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = client.post('/login/', data={"email": test_user.email, "password": "password123"})
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access_token']}")
        assert response.status_code == status.HTTP_200_OK

        response = client.post('/logout/')
        assert response.status_code == status.HTTP_200_OK

        with pytest.raises(TokenError):
            response = client.post('/logout/')
            assert response.status_code == status.HTTP_401_UNAUTHORIZED


def login(test_user, client):
    # Login
    login_response = client.post('/login/', data={"email": test_user.email, "password": "password123"})
    assert login_response.status_code == status.HTTP_200_OK

    access_token = login_response.data["access_token"]

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")


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
        login(test_user, client)

        # Post a review with valid data
        review_data = {
            "user": test_user.id,
            "listing": test_listing.id,
            "rating": 3,
            "comment": "Test Review"
        }
        response = client.post('/reviews/', data=review_data)

        assert response.status_code == status.HTTP_201_CREATED

        review_data["rating"] = 6
        response = client.post('/reviews/', data=review_data)

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

        response = client.post('/reviews/', data=review_data)

        # TODO: I get a 201 instead of a 400
        assert response.status_code == status.HTTP_400_BAD_REQUEST