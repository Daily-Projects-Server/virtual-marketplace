# Rest
from rest_framework import viewsets, permissions
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
    OpenApiExample,
    OpenApiParameter,
    OpenApiTypes,
)

# Local
from ..permissions import IsAllowedToReview, IsAllowedToDestroyReview
from ..serializers import ReviewSerializer
from ..models import Review


@extend_schema_view(
    list=extend_schema(
        summary="List all reviews",
        description="Returns a list of all reviews in the system.",
        responses={
            200: OpenApiResponse(
                response=ReviewSerializer(many=True),
                description="Successful response",
                examples=[
                    OpenApiExample(
                        "Example Response",
                        value=[
                            {
                                "id": 1,
                                "user": 1,
                                "listing": 1,
                                "rating": 5,
                                "comment": "Great product!",
                                "created_at": "2023-06-15T10:30:00Z",
                            },
                            {
                                "id": 2,
                                "user": 2,
                                "listing": 1,
                                "rating": 4,
                                "comment": "Good value for money.",
                                "created_at": "2023-06-16T14:45:00Z",
                            },
                        ],
                    )
                ],
            ),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
        },
        tags=["Reviews"],
    ),
    create=extend_schema(
        summary="Create a new review",
        description="Create a new review for a product or service.",
        request=ReviewSerializer,
        responses={
            201: OpenApiResponse(
                response=ReviewSerializer,
                description="Review created successfully",
                examples=[
                    OpenApiExample(
                        "Example Response",
                        value={
                            "id": 3,
                            "user": 3,
                            "listing": 2,
                            "rating": 5,
                            "comment": "Excellent service!",
                            "created_at": "2023-06-17T09:00:00Z",
                        },
                    )
                ],
            ),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
        },
        tags=["Reviews"],
    ),
    retrieve=extend_schema(
        summary="Retrieve a review",
        description="Get details of a specific review by ID.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="A unique integer value identifying this review.",
            )
        ],
        responses={
            200: OpenApiResponse(
                response=ReviewSerializer,
                description="Successful response",
                examples=[
                    OpenApiExample(
                        "Example Response",
                        value={
                            "id": 1,
                            "user": 1,
                            "listing": 1,
                            "rating": 5,
                            "comment": "Great product!",
                            "created_at": "2023-06-15T10:30:00Z",
                        },
                    )
                ],
            ),
            404: OpenApiResponse(description="Review not found"),
        },
        tags=["Reviews"],
    ),
    update=extend_schema(
        summary="Update a review",
        description="Update details of a specific review by ID.",
        request=ReviewSerializer,
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="A unique integer value identifying this review.",
            )
        ],
        responses={
            200: OpenApiResponse(
                response=ReviewSerializer,
                description="Review updated successfully",
                examples=[
                    OpenApiExample(
                        "Example Response",
                        value={
                            "id": 1,
                            "user": 1,
                            "listing": 1,
                            "rating": 4,
                            "comment": "Good product, but could be better.",
                            "created_at": "2023-06-15T10:30:00Z",
                        },
                    )
                ],
            ),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Review not found"),
        },
        tags=["Reviews"],
    ),
    partial_update=extend_schema(
        summary="Partially update a review",
        description="Partially update details of a specific review by ID.",
        request=ReviewSerializer,
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="A unique integer value identifying this review.",
            )
        ],
        responses={
            200: OpenApiResponse(
                response=ReviewSerializer,
                description="Review partially updated successfully",
                examples=[
                    OpenApiExample(
                        "Example Response",
                        value={
                            "id": 1,
                            "user": 1,
                            "listing": 1,
                            "rating": 4,
                            "comment": "Updated comment",
                            "created_at": "2023-06-15T10:30:00Z",
                        },
                    )
                ],
            ),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Review not found"),
        },
        tags=["Reviews"],
    ),
    destroy=extend_schema(
        summary="Delete a review",
        description="Delete a specific review by ID.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="A unique integer value identifying this review.",
            )
        ],
        responses={
            204: OpenApiResponse(description="Review deleted successfully"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Review not found"),
        },
        tags=["Reviews"],
    ),
)
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAllowedToReview,
        IsAllowedToDestroyReview,
    ]
