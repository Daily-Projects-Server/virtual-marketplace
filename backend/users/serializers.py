from django.contrib.auth import authenticate

from rest_framework import serializers

from .models import *


# Serializers define the API representation
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate_empty_values(self, data):
        return super().validate_empty_values(data)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')            
        
        user = authenticate(request=self.context.get('request'),
                            email=email, password=password)
        
        if not user:
            msg ='Unable to log in with provided credentials.'
            raise serializers.ValidationError(msg, code="authorization")
        
        data['user'] = user
        return data
    
class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name  = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()
    
    def validate_empty_values(self, data):
        return super().validate_empty_values(data)
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exits')
        
        return value
    
    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        
        if confirm_password != password:
            serializers.ValidationError("Confirm password does not match with password")
            
        return data
    
    def create(self, validated_data):
        return User.objects.create(**validated_data)
    
    
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


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
