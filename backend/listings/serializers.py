from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Category, Favorite, Listing


# Global functions
def is_negative(num):
    return num < 0


# Serializers
class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = "__all__"

    def validate_price(self, value):
        if is_negative(value):
            raise ValidationError("Price cannot be negative")
        return value

    def validate_quantity(self, value):
        if is_negative(value):
            raise ValidationError("Quantity cannot be negative")
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ["user", "listing"]
