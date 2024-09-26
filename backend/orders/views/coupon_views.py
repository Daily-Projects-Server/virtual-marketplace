from rest_framework import viewsets
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
    OpenApiExample,
)

from ..models import Coupon
from ..serializers import CouponSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List all coupons",
        description="Returns a list of all coupons in the system.",
        responses={
            200: OpenApiResponse(
                response=CouponSerializer(many=True),
                description="Successful response",
                examples=[
                    OpenApiExample(
                        "Example Response",
                        value=[
                            {
                                "id": 1,
                                "code": "BLACKFRIDAY",
                                "discount_percent": 20,
                                "valid_from": "2023-06-01T00:00:00Z",
                                "valid_to": "2023-08-31T23:59:59Z",
                                "is_active": True,
                            },
                            {
                                "id": 2,
                                "code": "WELCOME10",
                                "discount_percent": 10,
                                "valid_from": "2023-01-01T00:00:00Z",
                                "valid_to": "2023-12-31T23:59:59Z",
                                "is_active": True,
                            },
                        ],
                    )
                ],
            ),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
        },
        tags=["Coupons"],
    ),
    create=extend_schema(
        summary="Create a new coupon",
        description="Create a new coupon.",
        request=CouponSerializer,
        responses={
            201: OpenApiResponse(
                response=CouponSerializer,
                description="Coupon created successfully",
                examples=[
                    OpenApiExample(
                        "Example Response",
                        value={
                            "id": 3,
                            "code": "NEWYEAR2024",
                            "discount_percent": 15,
                            "valid_from": "2024-01-01T00:00:00Z",
                            "valid_to": "2024-01-31T23:59:59Z",
                            "is_active": True,
                        },
                    )
                ],
            ),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
        },
        tags=["Coupons"],
    ),
    retrieve=extend_schema(
        summary="Get a coupon by ID",
        description="Retrieve a coupon by its ID.",
        responses={
            200: OpenApiResponse(
                response=CouponSerializer,
                description="Successful response",
                examples=[
                    OpenApiExample(
                        "Example Response",
                        value={
                            "id": 1,
                            "code": "SUMMER2023",
                            "discount_percent": 20,
                            "valid_from": "2023-06-01T00:00:00Z",
                            "valid_to": "2023-08-31T23:59:59Z",
                            "is_active": True,
                        },
                    )
                ],
            ),
            404: OpenApiResponse(description="Coupon not found"),
        },
        tags=["Coupons"],
    ),
    update=extend_schema(
        summary="Update a coupon",
        description="Update a coupon by its ID.",
        request=CouponSerializer,
        responses={
            200: OpenApiResponse(
                response=CouponSerializer,
                description="Coupon updated successfully",
                examples=[
                    OpenApiExample(
                        "Example Response",
                        value={
                            "id": 1,
                            "code": "SUMMER2023_EXTENDED",
                            "discount_percent": 25,
                            "valid_from": "2023-06-01T00:00:00Z",
                            "valid_to": "2023-09-30T23:59:59Z",
                            "is_active": True,
                        },
                    )
                ],
            ),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Coupon not found"),
        },
        tags=["Coupons"],
    ),
    partial_update=extend_schema(
        summary="Partially update a coupon",
        description="Partially update a coupon by its ID.",
        request=CouponSerializer,
        responses={
            200: OpenApiResponse(
                response=CouponSerializer,
                description="Coupon partially updated successfully",
                examples=[
                    OpenApiExample(
                        "Example Response",
                        value={
                            "id": 1,
                            "code": "SUMMER2023",
                            "discount_percent": 20,
                            "valid_from": "2023-06-01T00:00:00Z",
                            "valid_to": "2023-09-15T23:59:59Z",
                            "is_active": True,
                        },
                    )
                ],
            ),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Coupon not found"),
        },
        tags=["Coupons"],
    ),
    destroy=extend_schema(
        summary="Delete a coupon",
        description="Delete a coupon by its ID.",
        responses={
            204: OpenApiResponse(description="Coupon deleted successfully"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
            404: OpenApiResponse(description="Coupon not found"),
        },
        tags=["Coupons"],
    ),
)
class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
