from rest_framework import serializers

from listings.models import Listing
from .models import *


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"

    # Add the listing and the cart when user posts
    def create(self, validated_data):
        listing = validated_data.pop("listing")
        cart = validated_data.pop("cart")
        cart_item = CartItem.objects.create(
            listing=listing, cart=cart, **validated_data
        )
        return cart_item

    def validate(self, attrs):
        listing = attrs["listing"]
        cart = attrs["cart"]
        quantity = int(attrs["quantity"])

        # Check  if the listing and cart are valid
        if not Listing.objects.filter(id=listing.id).exists():
            raise serializers.ValidationError("Listing does not exist")
        if not Cart.objects.filter(id=cart.id).exists():
            raise serializers.ValidationError("Cart does not exist")
        
        # Check if the listing is active
        if not listing.active:
            raise serializers.ValidationError("Listing is not active")

        # Check the quantity of the listing
        if quantity > listing.quantity:
            raise serializers.ValidationError(
                "Quantity is greater than the available quantity"
            )
        elif quantity < 1:
            raise serializers.ValidationError("Quantity cannot be less than 1")
        
        return attrs


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"
