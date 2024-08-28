from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets, mixins
<<<<<<< HEAD
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
=======
>>>>>>> upstream/main


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
<<<<<<< HEAD
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
=======
>>>>>>> upstream/main


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
<<<<<<< HEAD
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

    
=======
    serializer_class = CategorySerializer
>>>>>>> upstream/main
