import pytest
from django.contrib.auth import get_user_model
from .models import Settings

User = get_user_model()


class TestUserModel:
    @pytest.mark.django_db
    def test_create_user_with_valid_data(self):
        user = User.objects.create_user(email="test@example.com", password="password123", first_name="John",
                                        last_name="Doe")
        assert user.email == "test@example.com"
        assert user.check_password("password123")
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.settings is not None

    @pytest.mark.django_db
    def test_create_user_without_email_raises_error(self):
        with pytest.raises(ValueError, match="The Email field must be set"):
            User.objects.create_user(email="", password="password123")

    @pytest.mark.django_db
    def test_create_user_without_password_raises_error(self):
        with pytest.raises(ValueError, match="The Password field must be set"):
            User.objects.create_user(email="test@example.com", password="")

    @pytest.mark.django_db
    def test_create_superuser_with_valid_data(self):
        superuser = User.objects.create_superuser(email="admin@example.com", password="admin123", first_name="Admin",
                                                  last_name="User")
        assert superuser.is_staff
        assert superuser.is_superuser

    @pytest.mark.django_db
    def test_create_superuser_without_is_staff_raises_error(self):
        with pytest.raises(ValueError, match="Superuser must have is_staff=True."):
            User.objects.create_superuser(email="admin@example.com", password="admin123", is_staff=False)

    @pytest.mark.django_db
    def test_create_superuser_without_is_superuser_raises_error(self):
        with pytest.raises(ValueError, match="Superuser must have is_superuser=True."):
            User.objects.create_superuser(email="admin@example.com", password="admin123", is_superuser=False)

    @pytest.mark.django_db
    def test_user_has_perm_returns_true_for_superuser(self):
        superuser = User.objects.create_superuser(email="admin@example.com", password="admin123", first_name="Admin",
                                                  last_name="User")
        assert superuser.has_perm("any_perm")

    @pytest.mark.django_db
    def test_user_has_perms_returns_true_for_superuser(self):
        superuser = User.objects.create_superuser(email="admin@example.com", password="admin123", first_name="Admin",
                                                  last_name="User")
        assert superuser.has_perms(["perm1", "perm2"])

    @pytest.mark.django_db
    def test_user_email_is_lowercase_on_save(self):
        user = User.objects.create_user(email="TEST@EXAMPLE.COM", password="password123", first_name="John",
                                        last_name="Doe")
        assert user.email == "test@example.com"

    @pytest.mark.django_db
    def test_user_has_default_settings(self):
        user = User.objects.create_user(email="TEST@EXAMPLE.COM", password="password123", first_name="John",
                                        last_name="Doe")
        assert user.settings is not None
        assert user.settings.dark_mode is False

    @pytest.mark.django_db
    def test_total_number_of_settings_instances_are_one_when_all_users_have_default_settings(self):
        User.objects.create_user(email='user1@example.com', password='password1', first_name='John', last_name='Doe'),
        User.objects.create_user(email='user2@example.com', password='password2', first_name='Jane', last_name='Smith'),
        User.objects.create_user(email='user3@example.com', password='password3', first_name='Jim', last_name='Beam'),
        settings = Settings.objects.all()
        assert settings.count() == 1

    # TODO: Fix this test
    @pytest.mark.django_db
    def test_if_settings_instance_is_created_when_user_change_settings(self):
        user = User.objects.create_user(email="TEST@EXAMPLE.COM", password="password123", first_name="John",
                                        last_name="Doe")
        user.settings.dark_mode = True
        user.save()
        assert Settings.objects.count() == 2
