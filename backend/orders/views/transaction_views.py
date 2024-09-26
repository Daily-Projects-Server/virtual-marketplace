from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiExample

from ..models import Transaction
from ..serializers import TransactionSerializer

@extend_schema_view(
    list=extend_schema(
        summary="List all transactions",
        description="Returns a list of all transactions in the system.",
        responses={
            200: OpenApiResponse(
                response=TransactionSerializer(many=True),
                description="Successful response",
                examples=[
                    OpenApiExample(
                        'Example Response',
                        value=[
                            {
                                "id": 1,
                                "user": 1,
                                "items": [
                                    {"id": 1, "listing": 1, "quantity": 2},
                                    {"id": 2, "listing": 3, "quantity": 1}
                                ],
                                "total": "150.00",
                                "status": "completed",
                                "created_at": "2023-06-15T10:30:00Z",
                                "updated_at": "2023-06-15T10:30:00Z"
                            },
                            {
                                "id": 2,
                                "user": 2,
                                "items": [
                                    {"id": 3, "listing": 2, "quantity": 1}
                                ],
                                "total": "75.00",
                                "status": "pending",
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
        tags=["Transactions"],
    ),
    create=extend_schema(
        summary="Create a new transaction",
        description="Create a new transaction (order)",
        request=TransactionSerializer,
        responses={
            201: OpenApiResponse(
                response=TransactionSerializer,
                description="Transaction created successfully",
                examples=[
                    OpenApiExample(
                        'Example Response',
                        value={
                            "id": 3,
                            "user": 3,
                            "items": [
                                {"id": 4, "listing": 4, "quantity": 1}
                            ],
                            "total": "100.00",
                            "status": "pending",
                            "created_at": "2023-06-16T09:00:00Z",
                            "updated_at": "2023-06-16T09:00:00Z"
                        }
                    )
                ]
            ),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
        },
        tags=["Transactions"],
    ),
    retrieve=extend_schema(
        summary="Get a transaction by ID",
        description="Retrieve a transaction by its ID.",
        responses={
            200: OpenApiResponse(
                response=TransactionSerializer,
                description="Successful response",
                examples=[
                    OpenApiExample(
                        'Example Response',
                        value={
                            "id": 1,
                            "user": 1,
                            "items": [
                                {"id": 1, "listing": 1, "quantity": 2},
                                {"id": 2, "listing": 3, "quantity": 1}
                            ],
                            "total": "150.00",
                            "status": "completed",
                            "created_at": "2023-06-15T10:30:00Z",
                            "updated_at": "2023-06-15T10:30:00Z"
                        }
                    )
                ]
            ),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
            404: OpenApiResponse(description="Transaction not found"),
        },
        tags=["Transactions"],
    ),
    update=extend_schema(
        summary="Update a transaction",
        description="Update a transaction by its ID.",
        request=TransactionSerializer,
        responses={
            200: OpenApiResponse(
                response=TransactionSerializer,
                description="Transaction updated successfully",
                examples=[
                    OpenApiExample(
                        'Example Response',
                        value={
                            "id": 1,
                            "user": 1,
                            "items": [
                                {"id": 1, "listing": 1, "quantity": 3},
                                {"id": 2, "listing": 3, "quantity": 2}
                            ],
                            "total": "200.00",
                            "status": "completed",
                            "created_at": "2023-06-15T10:30:00Z",
                            "updated_at": "2023-06-16T11:00:00Z"
                        }
                    )
                ]
            ),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
            404: OpenApiResponse(description="Transaction not found"),
        },
        tags=["Transactions"],
    ),
    partial_update=extend_schema(
        summary="Partially update a transaction",
        description="Partially update a transaction by its ID.",
        request=TransactionSerializer,
        responses={
            200: OpenApiResponse(
                response=TransactionSerializer,
                description="Transaction partially updated successfully",
                examples=[
                    OpenApiExample(
                        'Example Response',
                        value={
                            "id": 1,
                            "user": 1,
                            "items": [
                                {"id": 1, "listing": 1, "quantity": 2},
                                {"id": 2, "listing": 3, "quantity": 1}
                            ],
                            "total": "150.00",
                            "status": "shipped",
                            "created_at": "2023-06-15T10:30:00Z",
                            "updated_at": "2023-06-16T14:00:00Z"
                        }
                    )
                ]
            ),
            400: OpenApiResponse(description="Bad request"),
            401: OpenApiResponse(description="Unauthorized"),
            404: OpenApiResponse(description="Transaction not found"),
        },
        tags=["Transactions"],
    ),
    destroy=extend_schema(
        summary="Delete a transaction",
        description="Delete a transaction by its ID.",
        responses={
            204: OpenApiResponse(description="Transaction deleted successfully"),
            401: OpenApiResponse(description="Unauthorized"),
            404: OpenApiResponse(description="Transaction not found"),
        },
        tags=["Transactions"],
    ),
)
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer