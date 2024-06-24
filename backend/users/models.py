from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from core.models import BaseModel


class User(AbstractBaseUser, BaseModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    address = models.ManyToManyField("Address", blank=True, related_name="user_addresses")
    settings = models.OneToOneField("Settings", on_delete=models.CASCADE, related_name="user_settings")

    # Specify the field that will be used as the unique identifier for the user
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.username = self.email

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Address(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="address_user")
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)

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
        return f"{self.user.username} favorite"


class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        return f"{self.user.username}'s review of {self.listing.title}"


class Message(BaseModel):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipient")
    message = models.TextField()

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"{self.sender.username} sent a message to {self.recipient.username}"


class Settings(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="settings_user")
    dark_mode = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Settings"
        verbose_name_plural = "Settings"

    def __str__(self):
        return f"{self.user.username}'s settings"
