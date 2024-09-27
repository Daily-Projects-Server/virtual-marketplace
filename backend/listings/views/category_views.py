from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework import viewsets
from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import IsAdminUser

from ..models import Category
from ..serializers import CategorySerializer


@extend_schema_view(
    list=extend_schema(
        summary="List all categories",
        description="Returns a list of all categories in the system.",
        responses={
            200: OpenApiResponse(
                response=CategorySerializer(many=True),
                description="Successful response",
                examples=[
                    OpenApiExample(
                        "Example Response",
                        value=[
                            {
                                "id": 1,
                                "name": "Electronics",
                                "description": "Electronic devices and gadgets",
                                "parent": None,
                            },
                            {
                                "id": 2,
                                "name": "Clothing",
                                "description": "Apparel and accessories",
                                "parent": None,
                            },
                        ],
                    )
                ],
            ),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
        },
        tags=["Categories"],
    ),
    create=extend_schema(
        summary="Create a new category",
        description="Create a new category.",
        request=CategorySerializer,
        responses={
            201: OpenApiResponse(
                response=CategorySerializer,
                description="Category created successfully",
                examples=[
                    OpenApiExample(
                        "Example Response",
                        value={
                            "id": 3,
                            "name": "Books",
                            "description": "Various types of books",
                            "parent": None,
                        },
                    )
                ],
            ),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
        },
        tags=["Categories"],
    ),
    retrieve=extend_schema(
        summary="Get a category by ID",
        description="Retrieve a category by its ID.",
        responses={
            200: OpenApiResponse(
                response=CategorySerializer,
                description="Successful response",
                examples=[
                    OpenApiExample(
                        "Example Response",
                        value={
                            "id": 1,
                            "name": "Electronics",
                            "description": "Electronic devices and gadgets",
                            "parent": None,
                        },
                    )
                ],
            ),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
            404: OpenApiResponse(description="Category not found"),
        },
        tags=["Categories"],
    ),
    update=extend_schema(
        summary="Update a category",
        description="Update a category by its ID.",
        request=CategorySerializer,
        responses={
            200: OpenApiResponse(
                response=CategorySerializer,
                description="Category updated successfully",
                examples=[
                    OpenApiExample(
                        "Example Response",
                        value={
                            "id": 1,
                            "name": "Electronics and Gadgets",
                            "description": "Updated description for electronic devices",
                            "parent": None,
                        },
                    )
                ],
            ),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Category not found"),
        },
        tags=["Categories"],
    ),
    partial_update=extend_schema(
        summary="Partially update a category",
        description="Partially update a category by its ID.",
        request=CategorySerializer,
        responses={
            200: OpenApiResponse(
                response=CategorySerializer,
                description="Category partially updated successfully",
                examples=[
                    OpenApiExample(
                        "Example Response",
                        value={
                            "id": 1,
                            "name": "Electronics",
                            "description": "Updated description for electronic devices",
                            "parent": None,
                        },
                    )
                ],
            ),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Category not found"),
        },
        tags=["Categories"],
    ),
    destroy=extend_schema(
        summary="Delete a category",
        description="Delete a category by its ID.",
        responses={
            204: OpenApiResponse(description="Category deleted successfully"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Category not found"),
        },
        tags=["Categories"],
    ),
)
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [
        TokenAuthentication,
        SessionAuthentication,
        BasicAuthentication,
    ]
    permission_classes = [IsAdminUser]
