from django.db import models
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from core.models import BaseModel


class Listing(BaseModel):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="listing_images/")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Track when the listing was created
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('archived', 'Archived'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')  # Track the status of the listing

    class Meta:
        verbose_name = "Listing"
        verbose_name_plural = "Listings"

    def clean(self):
        if self.price < 0:
            raise ValidationError("Price cannot be negative")
        if self.quantity < 0:
            raise ValidationError("Quantity cannot be negative")
        if self.owner is None:
            raise ValidationError("Owner is required")

    def close_listings(self):
        self.active = False

    def activate_listings(self):
        self.active = True

    def save(self, *args, **kwargs):
        self.full_clean()
        instance = super().save(*args, **kwargs)

        if self.quantity == 0:
            self.close_listings()
        elif self.quantity > 0 and not self.active:
            self.activate_listings()

        return instance

    def __str__(self):
        return self.title


class Category(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
