# Remote imports
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.exceptions import TokenError

# Local imports
from orders.models import Cart
from users.models import Settings
from users.common_for_tests import User, user_fixture, superuser_fixture


class TestUserModel:
    @pytest.mark.django_db
    def test_create_user_with_valid_data(self, user_fixture):
        assert user_fixture.email == "test@example.com"
        assert user_fixture.check_password("password123")
        assert user_fixture.first_name == "John"
        assert user_fixture.last_name == "Doe"
        assert user_fixture.settings is not None

    @pytest.mark.django_db
    def test_create_user_without_email_raises_error(self):
        with pytest.raises(ValueError, match="The Email field must be set"):
            User.objects.create_user(email="", password="password123")

    @pytest.mark.django_db
    def test_create_user_without_password_raises_error(self):
        with pytest.raises(ValueError, match="The Password field must be set"):
            User.objects.create_user(email="test@example.com", password="")

    @pytest.mark.django_db
    def test_create_superuser_with_valid_data(self, superuser_fixture):
        assert superuser_fixture.is_staff
        assert superuser_fixture.is_superuser

    @pytest.mark.django_db
    def test_create_superuser_without_is_staff_raises_error(self):
        with pytest.raises(ValueError, match="Superuser must have is_staff=True."):
            User.objects.create_superuser(
                email="admin@example.com", password="admin123", is_staff=False
            )

    @pytest.mark.django_db
    def test_create_superuser_without_is_superuser_raises_error(self):
        with pytest.raises(ValueError, match="Superuser must have is_superuser=True."):
            User.objects.create_superuser(
                email="admin@example.com", password="admin123", is_superuser=False
            )

    @pytest.mark.django_db
    def test_user_has_perm_returns_true_for_superuser(self, superuser_fixture):
        assert superuser_fixture.has_perm("any_perm")

    @pytest.mark.django_db
    def test_user_has_perms_returns_true_for_superuser(self, superuser_fixture):
        assert superuser_fixture.has_perms(["perm1", "perm2"])

    @pytest.mark.django_db
    def test_user_email_is_lowercase_on_save(self, user_fixture):
        assert user_fixture.email == "test@example.com"

    @pytest.mark.django_db
    def test_user_has_default_settings(self, user_fixture):
        assert user_fixture.settings is not None
        assert user_fixture.settings.dark_mode is False

    @pytest.mark.django_db
    def test_total_number_of_settings_instances_are_one_when_all_users_have_default_settings(
        self,
    ):
        User.objects.create_user(
            email="user1@example.com",
            password="password1",
            first_name="John",
            last_name="Doe",
        ),
        User.objects.create_user(
            email="user2@example.com",
            password="password2",
            first_name="Jane",
            last_name="Smith",
        ),
        User.objects.create_user(
            email="user3@example.com",
            password="password3",
            first_name="Jim",
            last_name="Beam",
        ),
        settings = Settings.objects.all()
        assert settings.count() == 1

    @pytest.mark.django_db
    def test_if_settings_instance_is_created_when_user_change_settings(
        self, user_fixture
    ):
        user_fixture.settings.dark_mode = True
        user_fixture.save()

        # Check if the settings instance is created and the dark_mode is True
        assert Settings.objects.count() == 2
        assert user_fixture.settings.id == 2
        assert Settings.objects.get(id=1).dark_mode is False
        assert Settings.objects.get(id=2).dark_mode is True
        assert user_fixture.settings.dark_mode is True

    @pytest.mark.django_db
    def test_if_settings_instance_is_not_deleted_when_user_is_deleted(
        self, user_fixture
    ):
        user_fixture = User.objects.create_user(
            email="test@test.com", password="password123"
        )
        user_fixture.delete()
        assert Settings.objects.count() == 1

    @pytest.mark.django_db
    def test_if_cart_is_created_when_user_is_created(self, user_fixture):
        assert user_fixture.cart is not None
        assert user_fixture.cart.buyer == user_fixture
        assert user_fixture.cart.cartitem_set.count() == 0
        assert Cart.objects.count() == 1


class TestUserViews:
    @pytest.mark.django_db
    def test_user_can_register(self, user_fixture):
        client = APIClient()
        register_url = reverse("register")

        # Register with without data
        response = client.post(register_url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Register with valid data
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
    def test_user_can_login(self, user_fixture):
        client = APIClient()
        login_url = reverse("login")

        # Login without data
        response = client.post(login_url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Login with valid data
        data = {
            "email": user_fixture.email,
            "password": "password123",
        }
        response = client.post(login_url, data=data)
        assert response.status_code == status.HTTP_200_OK

        # Login with invalid data
        data["password"] = "wrong-password"
        response = client.post(login_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_user_can_logout(self, user_fixture):
        client = APIClient()
        login_url = reverse("login")
        logout_url = reverse("logout")

        # Logout without authentication
        response = client.post(logout_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Logout with authentication
        response = client.post(
            login_url, data={"email": user_fixture.email, "password": "password123"}
        )
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access_token']}")
        assert response.status_code == status.HTTP_200_OK
        response = client.post(logout_url)
        assert response.status_code == status.HTTP_200_OK

        # Logout with blacklisted token
        with pytest.raises(TokenError):
            response = client.post(logout_url)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
