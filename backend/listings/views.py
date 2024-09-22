from .models import *
from .serializers import *
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view

from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication

@extend_schema_view(
    list=extend_schema(
        summary="List all listings",
        description="Returns a list of all listings in the system.",
        responses={200: ListingSerializer(many=True)},
        tags=["Listings"]
    ),
    create=extend_schema(
        summary="Create a new listing",
        description="Create a new listing.",
        request=ListingSerializer,
        responses={201: ListingSerializer},
        tags=["Listings"]
    ),
    retrieve=extend_schema(
        summary="Get a listing by ID",
        description="Retrieve a listing by its ID.",
        responses={200: ListingSerializer},
        tags=["Listings"]
    ),
    update=extend_schema(
        summary="Update a listing",
        description="Update a listing by its ID.",
        request=ListingSerializer,
        responses={200: ListingSerializer},
        tags=["Listings"]
    ),
    partial_update=extend_schema(
        summary="Partially update a listing",
        description="Partially update a listing by its ID.",
        request=ListingSerializer,
        responses={200: ListingSerializer},
        tags=["Listings"]
    ),
    destroy=extend_schema(
        summary="Delete a listing",
        description="Delete a listing by its ID.",
        responses={204: None},
        tags=["Listings"]
    )
)
class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

@extend_schema_view(
    list=extend_schema(
        summary="List all categories",
        description="Returns a list of all categories in the system.",
        responses={200: CategorySerializer(many=True)},
        tags=["Categories"]
    ),
    create=extend_schema(
        summary="Create a new category",    
        description="Create a new category.",
        request=CategorySerializer,
        responses={201: CategorySerializer},
        tags=["Categories"]
    ),
    retrieve=extend_schema(
        summary="Get a category by ID",
        description="Retrieve a category by its ID.",   
        responses={200: CategorySerializer},
        tags=["Categories"]
    ),
    update=extend_schema(
        summary="Update a category",
        description="Update a category by its ID.",
        request=CategorySerializer,
        responses={200: CategorySerializer},                    
        tags=["Categories"]
    ),
    partial_update=extend_schema(
        summary="Partially update a category",
        description="Partially update a category by its ID.",
        request=CategorySerializer,
        responses={200: CategorySerializer},
        tags=["Categories"]
    ),
    destroy=extend_schema(
        summary="Delete a category",
        description="Delete a category by its ID.",
        responses={204: None},
        tags=["Categories"]
    )
)
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser]

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
        summary="Get a favorite by ID",
        description="Retrieve a favorite by its ID for the authenticated user.",   
        responses={200: FavoriteSerializer},
        tags=["Favorites"]
    ),
    update=extend_schema(
        summary="Update a favorite",
        description="Update a favorite by its ID for the authenticated user.",
        request=FavoriteSerializer,
        responses={200: FavoriteSerializer},    
        tags=["Favorites"]
    ),
    partial_update=extend_schema(
        summary="Partially update a favorite",
        description="Partially update a favorite by its ID for the authenticated user.",
        request=FavoriteSerializer,
        responses={200: FavoriteSerializer},
        tags=["Favorites"]
    ),
    destroy=extend_schema(
        summary="Delete a favorite",
        description="Delete a favorite by its ID for the authenticated user.",
        responses={204: None},
        tags=["Favorites"]
    )
)
class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return favorites of the logged-in user
        return self.queryset.filter(user=self.request.user)
