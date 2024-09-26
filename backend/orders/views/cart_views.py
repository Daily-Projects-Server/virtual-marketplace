from rest_framework import viewsets
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
    OpenApiExample,
)

from ..permissions import IsNotAllowedToDestroy
from ..models import Cart
from ..serializers import CartSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List all carts",
        description="Returns a list of all carts in the system.",
        responses={
            200: OpenApiResponse(
                response=CartSerializer(many=True),
                description="Successful response",
                examples=[
                    OpenApiExample(
                        "Example Response",
                        value=[
                            {
                                "id": 1,
                                "user": 1,
                                "items": [
                                    {"id": 1, "listing": 1, "quantity": 2},
                                    {"id": 2, "listing": 3, "quantity": 1},
                                ],
                                "total": "150.00",
                                "created_at": "2023-06-15T10:30:00Z",
                                "updated_at": "2023-06-15T10:30:00Z",
                            },
                            {
                                "id": 2,
                                "user": 2,
                                "items": [{"id": 3, "listing": 2, "quantity": 1}],
                                "total": "75.00",
                                "created_at": "2023-06-15T11:00:00Z",
                                "updated_at": "2023-06-15T11:00:00Z",
                            },
                        ],
                    )
                ],
            ),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
        },
        tags=["Carts"],
    ),
    create=extend_schema(
        summary="Create a new cart",
        description="Create a new cart for a user.",
        request=CartSerializer,
        responses={
            201: OpenApiResponse(
                response=CartSerializer,
                description="Cart created successfully",
                examples=[
                    OpenApiExample(
                        "Example Response",
                        value={
                            "id": 3,
                            "user": 3,
                            "items": [],
                            "total": "0.00",
                            "created_at": "2023-06-15T12:00:00Z",
                            "updated_at": "2023-06-15T12:00:00Z",
                        },
                    )
                ],
            ),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
        },
        tags=["Carts"],
    ),
    retrieve=extend_schema(
        summary="Get a cart by ID",
        description="Retrieve a cart by its ID.",
        responses={
            200: OpenApiResponse(
                response=CartSerializer,
                description="Successful response",
                examples=[
                    OpenApiExample(
                        "Example Response",
                        value={
                            "id": 1,
                            "user": 1,
                            "items": [
                                {"id": 1, "listing": 1, "quantity": 2},
                                {"id": 2, "listing": 3, "quantity": 1},
                            ],
                            "total": "150.00",
                            "created_at": "2023-06-15T10:30:00Z",
                            "updated_at": "2023-06-15T10:30:00Z",
                        },
                    )
                ],
            ),
            404: OpenApiResponse(description="Cart not found"),
        },
        tags=["Carts"],
    ),
    update=extend_schema(
        summary="Update a cart",
        description="Update a cart by its ID.",
        request=CartSerializer,
        responses={
            200: OpenApiResponse(
                response=CartSerializer,
                description="Cart updated successfully",
                examples=[
                    OpenApiExample(
                        "Example Response",
                        value={
                            "id": 1,
                            "user": 1,
                            "items": [
                                {"id": 1, "listing": 1, "quantity": 3},
                                {"id": 2, "listing": 3, "quantity": 2},
                            ],
                            "total": "225.00",
                            "created_at": "2023-06-15T10:30:00Z",
                            "updated_at": "2023-06-15T13:00:00Z",
                        },
                    )
                ],
            ),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
            404: OpenApiResponse(description="Cart not found"),
        },
        tags=["Carts"],
    ),
    partial_update=extend_schema(
        summary="Partially update a cart",
        description="Partially update a cart by its ID.",
        request=CartSerializer,
        responses={
            200: OpenApiResponse(
                response=CartSerializer,
                description="Cart partially updated successfully",
                examples=[
                    OpenApiExample(
                        "Example Response",
                        value={
                            "id": 1,
                            "user": 1,
                            "items": [
                                {"id": 1, "listing": 1, "quantity": 2},
                                {"id": 2, "listing": 3, "quantity": 2},
                            ],
                            "total": "175.00",
                            "created_at": "2023-06-15T10:30:00Z",
                            "updated_at": "2023-06-15T14:00:00Z",
                        },
                    )
                ],
            ),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
            404: OpenApiResponse(description="Cart not found"),
        },
        tags=["Carts"],
    ),
    destroy=extend_schema(
        summary="Delete a cart",
        description="Delete a cart by its ID.",
        responses={
            204: OpenApiResponse(description="Cart deleted successfully"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Cart not found"),
        },
        tags=["Carts"],
    ),
)
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsNotAllowedToDestroy]
