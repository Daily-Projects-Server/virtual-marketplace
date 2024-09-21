from django.contrib.auth import authenticate

from rest_framework import serializers

from orders.models import Cart
from .models import *


# Serializers define the API representation
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # Debugging
        if not email or not password:
            raise serializers.ValidationError('Must include "email" and "password".')

        user = authenticate(request=self.context.get('request'),
                            email=email, password=password)

        if not user:
            msg = 'Unable to log in with provided credentials.'
            raise serializers.ValidationError(msg, code="authorization")

        data['user'] = user
        return data

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError('Invalid login credentials')
        return user


def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise serializers.ValidationError('Email already exits')

    return value


def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise serializers.ValidationError('Email already exits')

    return value


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'confirm_password']

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if confirm_password != password:
            raise serializers.ValidationError("Confirm password does not match with password")

        return data

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        # remove confirm_password
        validated_data.pop('confirm_password')

        return User.objects.create_user(email, password, **validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"

    def validate(self, attrs):
        if not attrs.get('rating') in range(1, 6):
            raise serializers.ValidationError('Rating must be between 1 and 5')
        return attrs

    def save(self, **kwargs):
        listing = kwargs.get('listing')
        user = kwargs.get('user')
        rating = self.validated_data.get('rating')
        review = Review.objects.filter(listing=listing, user=user).first()
        if review:
            review.rating = rating
            review.save()
        else:
            super().save(**kwargs)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
