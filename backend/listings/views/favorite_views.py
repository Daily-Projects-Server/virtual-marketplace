from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..models import Favorite
from ..serializers import FavoriteSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List all favorites",
        description="Returns a list of all favorites for the authenticated user.",
        responses={
            200: OpenApiResponse(
                response=FavoriteSerializer(many=True),
                description="Successful response",
                examples=[
                    OpenApiExample(
                        "Example Response",
                        value=[
                            {
                                "id": 1,
                                "user": 1,
                                "listing": 1,
                                "created_at": "2023-06-15T10:30:00Z",
                            },
                            {
                                "id": 2,
                                "user": 1,
                                "listing": 3,
                                "created_at": "2023-06-16T14:45:00Z",
                            },
                        ],
                    )
                ],
            ),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
        },
        tags=["Favorites"],
    ),
    create=extend_schema(
        summary="Create a new favorite",
        description="Create a new favorite for the authenticated user.",
        request=FavoriteSerializer,
        responses={
            201: OpenApiResponse(
                response=FavoriteSerializer,
                description="Favorite created successfully",
                examples=[
                    OpenApiExample(
                        "Example Response",
                        value={
                            "id": 3,
                            "user": 1,
                            "listing": 5,
                            "created_at": "2023-06-17T09:00:00Z",
                        },
                    )
                ],
            ),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
        },
        tags=["Favorites"],
    ),
    retrieve=extend_schema(
        summary="Get a favorite by ID",
        description="Retrieve a favorite by its ID for the authenticated user.",
        responses={
            200: OpenApiResponse(
                response=FavoriteSerializer,
                description="Successful response",
                examples=[
                    OpenApiExample(
                        "Example Response",
                        value={
                            "id": 1,
                            "user": 1,
                            "listing": 1,
                            "created_at": "2023-06-15T10:30:00Z",
                        },
                    )
                ],
            ),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
            404: OpenApiResponse(description="Favorite not found"),
        },
        tags=["Favorites"],
    ),
    update=extend_schema(
        summary="Update a favorite",
        description="Update a favorite by its ID for the authenticated user.",
        request=FavoriteSerializer,
        responses={
            200: OpenApiResponse(
                response=FavoriteSerializer,
                description="Favorite updated successfully",
                examples=[
                    OpenApiExample(
                        "Example Response",
                        value={
                            "id": 1,
                            "user": 1,
                            "listing": 2,
                            "created_at": "2023-06-15T10:30:00Z",
                        },
                    )
                ],
            ),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
            404: OpenApiResponse(description="Favorite not found"),
        },
        tags=["Favorites"],
    ),
    partial_update=extend_schema(
        summary="Partially update a favorite",
        description="Partially update a favorite by its ID for the authenticated user.",
        request=FavoriteSerializer,
        responses={
            200: OpenApiResponse(
                response=FavoriteSerializer,
                description="Favorite partially updated successfully",
                examples=[
                    OpenApiExample(
                        "Example Response",
                        value={
                            "id": 1,
                            "user": 1,
                            "listing": 2,
                            "created_at": "2023-06-15T10:30:00Z",
                        },
                    )
                ],
            ),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
            404: OpenApiResponse(description="Favorite not found"),
        },
        tags=["Favorites"],
    ),
    destroy=extend_schema(
        summary="Delete a favorite",
        description="Delete a favorite by its ID for the authenticated user.",
        responses={
            204: OpenApiResponse(description="Favorite deleted successfully"),
            401: OpenApiResponse(description="Unauthorized"),
            404: OpenApiResponse(description="Favorite not found"),
        },
        tags=["Favorites"],
    ),
)
class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return favorites of the logged-in user
        return self.queryset.filter(user=self.request.user)
