from django.db import models
from rest_framework.exceptions import ValidationError

from core.models import BaseModel
from users.models import User


class Listing(BaseModel):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="listing_images/")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Listing"
        verbose_name_plural = "Listings"
        constraints = [
            models.CheckConstraint(
                check=models.Q(price__gte=0), name="price_non_negative"
            )
        ]

    def clean(self):
        if self.price < 0:
            raise ValidationError("Price cannot be negative")
        if self.quantity < 0:
            raise ValidationError("Quantity cannot be negative")
        if self.owner is None:
            raise ValidationError("Owner is required")

    def close_listings(self):
        self.active = False

    @property
    def is_out_of_stock(self):
        return self.quantity == 0

    def activate_listings(self):
        self.active = True

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


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="favorited_by"
    )

    class Meta:
        unique_together = ("user", "listing")
        verbose_name = "Favorite"
        verbose_name_plural = "Favorites"

    def __str__(self):
        return f"{self.user.email} - {self.listing.title}"
