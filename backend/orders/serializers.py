from rest_framework import serializers

from .models import Cart, CartItem, Coupon, Transaction


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

    def validate(self, attrs):
        listing = attrs.get("listing")
        cart = attrs.get("cart")
        quantity = attrs.get("quantity")

        # If this is an update operation, get the existing instance
        instance = getattr(self, "instance", None)

        # Check the quantity of the listing
        if quantity is not None:
            if quantity > listing.quantity:
                raise serializers.ValidationError(
                    "Quantity is greater than the available quantity"
                )
            elif quantity < 1:
                raise serializers.ValidationError("Quantity cannot be less than 1")

        # Check if the cart exists
        if not cart:
            raise serializers.ValidationError("Cart does not exist")

        # Check if the item already exists in the cart (only for create operations)
        if (
            not instance
            and CartItem.objects.filter(cart=cart, listing=listing).exists()
        ):
            raise serializers.ValidationError("Item already exists in cart")

        # Check if the cart belongs to the user
        if cart and cart.buyer != self.context["request"].user:
            raise serializers.ValidationError("Cart does not belong to the user")

        # Check the listing
        if not listing:
            raise serializers.ValidationError("Listing does not exist")
        elif not listing.active:
            raise serializers.ValidationError("Listing is not active")

        return attrs

    def create(self, validated_data):
        return CartItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get("quantity", instance.quantity)
        instance.save()
        return instance


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"
