from django.db import models

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

    class Meta:
        verbose_name = "Listing"
        verbose_name_plural = "Listings"

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
