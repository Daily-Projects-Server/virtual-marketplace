from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication,
)

from ..models import Listing
from ..serializers import ListingSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List all listings",
        description="Returns a list of all listings in the system.",
        responses={200: ListingSerializer(many=True)},
        tags=["Listings"],
    ),
    create=extend_schema(
        summary="Create a new listing",
        description="Create a new listing.",
        request=ListingSerializer,
        responses={201: ListingSerializer},
        tags=["Listings"],
    ),
    retrieve=extend_schema(
        summary="Get a listing by ID",
        description="Retrieve a listing by its ID.",
        responses={200: ListingSerializer},
        tags=["Listings"],
    ),
    update=extend_schema(
        summary="Update a listing",
        description="Update a listing by its ID.",
        request=ListingSerializer,
        responses={200: ListingSerializer},
        tags=["Listings"],
    ),
    partial_update=extend_schema(
        summary="Partially update a listing",
        description="Partially update a listing by its ID.",
        request=ListingSerializer,
        responses={200: ListingSerializer},
        tags=["Listings"],
    ),
    destroy=extend_schema(
        summary="Delete a listing",
        description="Delete a listing by its ID.",
        responses={204: None},
        tags=["Listings"],
    ),
)
class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    authentication_classes = [
        TokenAuthentication,
        SessionAuthentication,
        BasicAuthentication,
    ]
    permission_classes = [IsAuthenticated]
