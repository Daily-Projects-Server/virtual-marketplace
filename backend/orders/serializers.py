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

    # def to_representation(self, instance):
    #    response = super().to_representation(instance)
    #    response['cart_items'] = CartItemSerializer(instance.cartitem_set.all(), many=True).data
    #    return response

    #def to_representation(self, instance):
    #    response = super().to_representation(instance)
    #    response['cart_items'] = CartItemSerializer(instance.cartitem_set.all(), many=True).data
    #    return response


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

        # Check the quantity of the listing
        if quantity > listing.quantity:
            raise serializers.ValidationError(
                "Quantity is greater than the available quantity"
            )
        elif quantity < 1:
            raise serializers.ValidationError("Quantity cannot be less than 1")

        # Check if the cart exists
        if not Cart.objects.filter(id=cart.id).exists():
            raise serializers.ValidationError("Cart does not exist")

        # Check the listing
        if not listing.active:
            raise serializers.ValidationError("Listing is not active")
        return attrs


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"
