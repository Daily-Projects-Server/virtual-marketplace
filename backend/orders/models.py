from django.db import models
from core.models import BaseModel


class Transaction(BaseModel):
    buyer = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="buyer")
    seller = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="seller")
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, null=False)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self):
        return f"{self.buyer.email} bought {self.quantity} of {self.listing.title} from {self.seller.email}"


class Cart(BaseModel):
    buyer = models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"{self.buyer.email}'s cart"


class CartItem(BaseModel):
    cart = models.ManyToManyField(to=Cart)
    listing = models.ManyToManyField(to='listings.Listing')
    quantity = models.PositiveSmallIntegerField(default=1, null=False)

    def __str__(self):
        return f"{self.quantity} of {self.listing.title} in {self.cart.buyer.email}'s cart"


class Coupon(BaseModel):
    code = models.CharField(max_length=255, null=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    active = models.BooleanField(default=True, null=False)

    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"

    def __str__(self):
        return self.code
