from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets, mixins

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from users.permissions import IsOwnerOrReadOnly


class ListingsView(APIView):
    permission_classes = [IsOwnerOrReadOnly]



class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        # Only the owner can update the status
        if 'status' in serializer.validated_data and self.request.user != serializer.instance.owner:
            raise PermissionDenied("You do not have permission to change the status of this listing.")

        serializer.save()

    def perform_create(self, serializer):
        # Ensure that the listing owner is set to the current user
        serializer.save(owner=self.request.user)



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser]

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return favorites of the logged-in user
        return self.queryset.filter(user=self.request.user)
