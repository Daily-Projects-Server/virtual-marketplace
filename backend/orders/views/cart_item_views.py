from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiExample

from ..permissions import IsNotItemAlreadyInCart
from ..models import CartItem
from ..serializers import CartItemSerializer

@extend_schema_view(
    list=extend_schema(
        summary="List all cart items",
        description="Returns a list of all cart items in the system.",
        responses={
            200: OpenApiResponse(
                response=CartItemSerializer(many=True),
                description="Successful response",
                examples=[
                    OpenApiExample(
                        'Example Response',
                        value=[
                            {
                                "id": 1,
                                "cart": 1,
                                "listing": 1,
                                "quantity": 2,
                                "created_at": "2023-06-15T10:30:00Z",
                                "updated_at": "2023-06-15T10:30:00Z"
                            },
                            {
                                "id": 2,
                                "cart": 1,
                                "listing": 2,
                                "quantity": 1,
                                "created_at": "2023-06-15T11:00:00Z",
                                "updated_at": "2023-06-15T11:00:00Z"
                            }
                        ]
                    )
                ]
            ),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
        },
        tags=["Cart Items"],
    ),
    create=extend_schema(
        summary="Create a new cart item",
        description="Create a new cart item for a cart.",
        request=CartItemSerializer,
        responses={
            201: OpenApiResponse(
                response=CartItemSerializer,
                description="Cart item created successfully",
                examples=[
                    OpenApiExample(
                        'Example Response',
                        value={
                            "id": 3,
                            "cart": 1,
                            "listing": 3,
                            "quantity": 1,
                            "created_at": "2023-06-15T12:00:00Z",
                            "updated_at": "2023-06-15T12:00:00Z"
                        }
                    )
                ]
            ),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
        },
        tags=["Cart Items"],
    ),
    retrieve=extend_schema(
        summary="Get a cart item by ID",
        description="Retrieve a cart item by its ID.",
        responses={
            200: OpenApiResponse(
                response=CartItemSerializer,
                description="Successful response",
                examples=[
                    OpenApiExample(
                        'Example Response',
                        value={
                            "id": 1,
                            "cart": 1,
                            "listing": 1,
                            "quantity": 2,
                            "created_at": "2023-06-15T10:30:00Z",
                            "updated_at": "2023-06-15T10:30:00Z"
                        }
                    )
                ]
            ),
            404: OpenApiResponse(description="Cart item not found"),
        },
        tags=["Cart Items"],
    ),
    update=extend_schema(
        summary="Update a cart item",
        description="Update a cart item by its ID.",
        request=CartItemSerializer,
        responses={
            200: OpenApiResponse(
                response=CartItemSerializer,
                description="Cart item updated successfully",
                examples=[
                    OpenApiExample(
                        'Example Response',
                        value={
                            "id": 1,
                            "cart": 1,
                            "listing": 1,
                            "quantity": 3,
                            "created_at": "2023-06-15T10:30:00Z",
                            "updated_at": "2023-06-15T13:00:00Z"
                        }
                    )
                ]
            ),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Cart item not found"),
        },
        tags=["Cart Items"],
    ),
    partial_update=extend_schema(
        summary="Partially update a cart item",
        description="Partially update a cart item by its ID.",
        request=CartItemSerializer,
        responses={
            200: OpenApiResponse(
                response=CartItemSerializer,
                description="Cart item partially updated successfully",
                examples=[
                    OpenApiExample(
                        'Example Response',
                        value={
                            "id": 1,
                            "cart": 1,
                            "listing": 1,
                            "quantity": 4,
                            "created_at": "2023-06-15T10:30:00Z",
                            "updated_at": "2023-06-15T14:00:00Z"
                        }
                    )
                ]
            ),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Cart item not found"),
        },
        tags=["Cart Items"],
    ),
    destroy=extend_schema(
        summary="Delete a cart item",
        description="Delete a cart item by its ID.",
        responses={
            204: OpenApiResponse(description="Cart item deleted successfully"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Cart item not found"),
        },
        tags=["Cart Items"],
    ),
)
class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsNotItemAlreadyInCart]