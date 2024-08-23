from rest_framework import serializers
from .models import *


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
