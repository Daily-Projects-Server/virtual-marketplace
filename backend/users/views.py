# Rest
from rest_framework import viewsets, mixins

# Local
from .permissions import *
from .serializers import *


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
<<<<<<< HEAD
    serializer_class = AddressSerializer
=======
    serializers_class = AddressSerializer
>>>>>>> upstream/main
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
<<<<<<< HEAD
    serializer_class = FavoriteSerializer
=======
    serializers_class = FavoriteSerializer
>>>>>>> upstream/main
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = Review.objects.all()
    serializers_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        listing = self.request.data.get('listing')
        serializer.save(user=self.request.user, listing=listing)
