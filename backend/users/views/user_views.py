from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
    extend_schema_view,
)
from rest_framework import viewsets

from ..models import User
from ..serializers import UserListSerializer, UserSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List all users",
        description="Returns a list of all active users in the system.",
        parameters=[
            OpenApiParameter(
                name="username",
                description="Filter by username",
                required=False,
                type=str,
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Successful response",
                examples=[
                    OpenApiExample(
                        "User List",
                        value=[
                            {
                                "id": 4,
                                "first_name": "John",
                                "last_name": "Doe",
                                "email": "john.doe@example.com",
                            },
                            {
                                "id": 5,
                                "first_name": "Jane",
                                "last_name": "Doe",
                                "email": "jane.doe@example.com",
                            },
                        ],
                        status_codes=["200"],
                    ),
                ],
            ),
        },
        tags=["Users"],
    ),
    retrieve=extend_schema(
        summary="Retrieve a user",
        description="Get details of a specific user by ID.",
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Successful response",
                examples=[
                    OpenApiExample(
                        "User Details",
                        value={
                            "id": 1,
                            "first_name": "test",
                            "last_name": "name",
                            "email": "test@email.com",
                            "is_staff": False,
                            "is_superuser": False,
                            "created": "2024-09-26T00:08:46.611164Z",
                            "modified": "2024-09-26T00:08:46.611164Z",
                            "last_login": None,
                        },
                        status_codes=["200"],
                    ),
                ],
            ),
            404: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="User not found",
                examples=[
                    OpenApiExample(
                        "User Not Found",
                        value={"detail": "No User matches the given query."},
                        status_codes=["404"],
                    ),
                ],
            ),
        },
        tags=["Users"],
    ),
)
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return UserListSerializer
        return UserSerializer
