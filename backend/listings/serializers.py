from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import *


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = "__all__"

    def validate_price(self, value):
        if value < 0:
            raise ValidationError("Price cannot be negative")
        return value

    def validate_quantity(self, value):
        if value < 0:
            raise ValidationError("Quantity cannot be negative")
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['user', 'listing']
