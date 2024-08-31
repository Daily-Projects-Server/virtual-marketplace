from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from core.models import BaseModel


# Manager for the User model
class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        # Validation
        if not email:
            raise ValueError("The Email field must be set")
        elif not password:
            raise ValueError("The Password field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email=email)


# Models
class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    settings = models.ForeignKey('Settings', on_delete=models.CASCADE, null=True, blank=True, unique=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    # Specify the fields that will be required when creating a superuser
    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    # Required methods
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_perms(self, perm_list, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def save(self, *args, **kwargs):
        self.email = self.email.lower()

        # Ensure the user's settings are set
        if not self.settings:
            self.settings = Settings.objects.get_or_create(id=1)[0]

        instance = super(User, self).save(*args, **kwargs)

        default_settings = Settings.objects.get(id=1)
        fields = [field for field in Settings._meta.get_fields()
                  if field.concrete
                  and not field.many_to_many
                  and field is not Settings._meta.pk]

        # Check if the user's settings differ from the default settings
        fields_differ = any(
            getattr(self.settings, field.name) != getattr(default_settings, field.name)
            for field in fields)

        # If the settings differ, create a new settings object for the user
        if fields_differ:
            new_settings = Settings.objects.create(
                **{field.name: getattr(self.settings, field.name) for field in fields}
            )
            self.settings = new_settings
            super(User, self).save(*args, **kwargs)

        return instance

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Address(BaseModel):
    street = models.CharField(max_length=255, null=False)
    city = models.CharField(max_length=255, null=False)
    state = models.CharField(max_length=255, null=False)
    zip_code = models.CharField(max_length=10, null=False)
    user = models.ManyToManyField(to=User)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state} {self.zip_code}"


class Favorite(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Favorite"
        verbose_name_plural = "Favorites"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} favorite"


class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}'s review of {self.listing.title}"


class Message(BaseModel):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipient")
    message = models.TextField()

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return (f"{self.sender.first_name} {self.sender.last_name} "
                f"sent a message to {self.recipient.first_name} "
                f"{self.recipient.last_name}")


class Settings(BaseModel):
    dark_mode = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Settings"
        verbose_name_plural = "Settings"

    def __str__(self):
        return f"{self.dark_mode}"
