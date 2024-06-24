from django.db import models
from core.models import BaseModel


class Transaction(BaseModel):
    buyer = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="buyer")
    seller = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="seller")
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self):
        return f"{self.buyer.username} bought {self.quantity} of {self.listing.title} from {self.seller.username}"


class Cart(BaseModel):
    buyer = models.ForeignKey('users.User', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    listings = models.ManyToManyField('listings.Listing')

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"{self.buyer.username}'s cart"


class Coupon(BaseModel):
    code = models.CharField(max_length=255)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"

    def __str__(self):
        return self.code
