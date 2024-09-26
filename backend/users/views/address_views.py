# Rest
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiExample
from drf_spectacular.types import OpenApiTypes

# Local
from ..permissions import IsOwnerOrReadOnly
from ..serializers import AddressSerializer
from ..models import Address

@extend_schema_view(
    list=extend_schema(
        summary="List all addresses",
        description="Returns a list of all addresses in the system.",
        responses={
            200: OpenApiResponse(
                response=AddressSerializer(many=True),
                description="Successful retrieval of addresses",
                examples=[
                    OpenApiExample(
                        'Successful Response',
                        value=[
                            {
                                "id": 1,
                                "street": "123 Main St",
                                "city": "Anytown",
                                "state": "CA",
                                "zip_code": "12345",
                                "country": "USA",
                                "user": 1
                            },
                            {
                                "id": 2,
                                "street": "456 Elm St",
                                "city": "Othertown",
                                "state": "NY",
                                "zip_code": "67890",
                                "country": "USA",
                                "user": 2
                            }
                        ],
                        status_codes=['200']
                    ),
                ]
            ),
            401: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Unauthorized",
                examples=[
                    OpenApiExample(
                        'Unauthorized',
                        value={"detail": "Authentication credentials were not provided."},
                        status_codes=['401']
                    ),
                ]
            ),
        },
        tags=["Addresses"]
    ),
    create=extend_schema(
        summary="Create a new address",
        description="Create a new address for the authenticated user.",
        request=AddressSerializer,
        responses={
            201: OpenApiResponse(
                response=AddressSerializer,
                description="Address created successfully",
                examples=[
                    OpenApiExample(
                        'Successful Response',
                        value={
                            "id": 3,
                            "street": "789 Oak St",
                            "city": "Newtown",
                            "state": "TX",
                            "zip_code": "54321",
                            "country": "USA",
                            "user": 1
                        },
                        status_codes=['201']
                    ),
                ]
            ),
            400: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Bad Request",
                examples=[
                    OpenApiExample(
                        'Bad Request',
                        value={"street": ["This field is required."]},
                        status_codes=['400']
                    ),
                ]
            ),
            401: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Unauthorized",
                examples=[
                    OpenApiExample(
                        'Unauthorized',
                        value={"detail": "Authentication credentials were not provided."},
                        status_codes=['401']
                    ),
                ]
            ),
        },
        tags=["Addresses"]
    ),
    retrieve=extend_schema(
        summary="Retrieve an address",
        description="Get details of a specific address by ID.",
        responses={
            200: OpenApiResponse(
                response=AddressSerializer,
                description="Successful retrieval of address",
                examples=[
                    OpenApiExample(
                        'Successful Response',
                        value={
                            "id": 1,
                            "street": "123 Main St",
                            "city": "Anytown",
                            "state": "CA",
                            "zip_code": "12345",
                            "country": "USA",
                            "user": 1
                        },
                        status_codes=['200']
                    ),
                ]
            ),
            404: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Not Found",
                examples=[
                    OpenApiExample(
                        'Not Found',
                        value={"detail": "Not found."},
                        status_codes=['404']
                    ),
                ]
            ),
        },
        tags=["Addresses"]
    ),
    update=extend_schema(
        summary="Update an address",
        description="Update details of a specific address by ID.",
        request=AddressSerializer,
        responses={
            200: OpenApiResponse(
                response=AddressSerializer,
                description="Address updated successfully",
                examples=[
                    OpenApiExample(
                        'Successful Response',
                        value={
                            "id": 1,
                            "street": "123 Updated St",
                            "city": "Newtown",
                            "state": "CA",
                            "zip_code": "12345",
                            "country": "USA",
                            "user": 1
                        },
                        status_codes=['200']
                    ),
                ]
            ),
            400: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Bad Request",
                examples=[
                    OpenApiExample(
                        'Bad Request',
                        value={"street": ["This field may not be blank."]},
                        status_codes=['400']
                    ),
                ]
            ),
            404: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Not Found",
                examples=[
                    OpenApiExample(
                        'Not Found',
                        value={"detail": "Not found."},
                        status_codes=['404']
                    ),
                ]
            ),
        },
        tags=["Addresses"]
    ),
    partial_update=extend_schema(
        summary="Partially update an address",
        description="Partially update details of a specific address by ID.",
        request=AddressSerializer,
        responses={
            200: OpenApiResponse(
                response=AddressSerializer,
                description="Address partially updated successfully",
                examples=[
                    OpenApiExample(
                        'Successful Response',
                        value={
                            "id": 1,
                            "street": "123 Main St",
                            "city": "Updated City",
                            "state": "CA",
                            "zip_code": "12345",
                            "country": "USA",
                            "user": 1
                        },
                        status_codes=['200']
                    ),
                ]
            ),
            400: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Bad Request",
                examples=[
                    OpenApiExample(
                        'Bad Request',
                        value={"city": ["This field may not be blank."]},
                        status_codes=['400']
                    ),
                ]
            ),
            404: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Not Found",
                examples=[
                    OpenApiExample(
                        'Not Found',
                        value={"detail": "Not found."},
                        status_codes=['404']
                    ),
                ]
            ),
        },
        tags=["Addresses"]
    ),
    destroy=extend_schema(
        summary="Delete an address",
        description="Delete a specific address by ID.",
        responses={
            204: OpenApiResponse(
                response=None,
                description="Address deleted successfully"
            ),
            404: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Not Found",
                examples=[
                    OpenApiExample(
                        'Not Found',
                        value={"detail": "Not found."},
                        status_codes=['404']
                    ),
                ]
            ),
        },
        tags=["Addresses"]
    )
)
class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)