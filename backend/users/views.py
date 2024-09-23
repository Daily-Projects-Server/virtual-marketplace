# Rest
from rest_framework import viewsets, permissions
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view

# Local
from .permissions import IsOwnerOrReadOnly, IsAllowedToReview, IsAllowedToDestroyReview
from .serializers import *
from .models import User


@extend_schema_view(
    list=extend_schema(
        summary="List all users",
        description="Returns a list of all active users in the system.",
        parameters=[
            OpenApiParameter(
                name='username', description='Filter by username', required=False, type=str),
        ],
        responses={200: UserSerializer(many=True)},
        tags=["Users"]
    ),
    retrieve=extend_schema(
        summary="Retrieve a user",
        description="Get details of a specific user by ID.",
        tags=["Users"]
    ),
)
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List all addresses",
        description="Returns a list of all addresses in the system.",
        responses={200: AddressSerializer(many=True)},
        tags=["Addresses"]
    ),
    create=extend_schema(
        summary="Create a new address",
        description="Create a new address for the authenticated user.",
        request=AddressSerializer,
        responses={201: AddressSerializer},
        tags=["Addresses"]
    ),
    retrieve=extend_schema(
        summary="Retrieve an address",
        description="Get details of a specific address by ID.",
        tags=["Addresses"]
    ),
    update=extend_schema(
        summary="Update an address",
        description="Update details of a specific address by ID.",
        tags=["Addresses"]
    ),
    partial_update=extend_schema(
        summary="Partially update an address",
        description="Partially update details of a specific address by ID.",
        tags=["Addresses"]
    ),
    destroy=extend_schema(
        summary="Delete an address",
        description="Delete a specific address by ID.",
        tags=["Addresses"]
    )
)
class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema_view(
    list=extend_schema(
        summary="List all favorites",
        description="Returns a list of all favorites for the authenticated user.",
        responses={200: FavoriteSerializer(many=True)},
        tags=["Favorites"]
    ),
    create=extend_schema(
        summary="Create a new favorite",
        description="Create a new favorite for the authenticated user.",
        request=FavoriteSerializer,
        responses={201: FavoriteSerializer},
        tags=["Favorites"]
    ),
    retrieve=extend_schema(
        summary="Retrieve a favorite",
        description="Get details of a specific favorite by ID.",
        tags=["Favorites"]
    ),
    update=extend_schema(
        summary="Update a favorite",
        description="Update details of a specific favorite by ID.",
        tags=["Favorites"]
    ),
    partial_update=extend_schema(
        summary="Partially update a favorite",
        description="Partially update details of a specific favorite by ID.",
        tags=["Favorites"]
    ),
    destroy=extend_schema(
        summary="Delete a favorite",
        description="Delete a specific favorite by ID.",
        tags=["Favorites"]
    ),
)
class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema_view(
    list=extend_schema(
        summary="List all reviews",
        description="Returns a list of all reviews in the system.",
        responses={200: ReviewSerializer(many=True)},
        tags=["Reviews"]
    ),
    create=extend_schema(
        summary="Create a new review",
        description="Create a new review for a product or service.",
        request=ReviewSerializer,
        responses={201: ReviewSerializer},
        tags=["Reviews"]
    ),
    retrieve=extend_schema(
        summary="Retrieve a review",
        description="Get details of a specific review by ID.",
        tags=["Reviews"]
    ),
    update=extend_schema(
        summary="Update a review",
        description="Update details of a specific review by ID.",
        tags=["Reviews"]
    ),
    partial_update=extend_schema(
        summary="Partially update a review",
        description="Partially update details of a specific review by ID.",
        tags=["Reviews"]
    ),
    destroy=extend_schema(
        summary="Delete a review",
        description="Delete a specific review by ID.",
        tags=["Reviews"]
    ),
)
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAllowedToReview, IsAllowedToDestroyReview]
