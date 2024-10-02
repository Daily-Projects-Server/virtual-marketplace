from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import viewsets

from ..models import User
from ..serializers import UserSerializer


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
        responses={200: UserSerializer(many=True)},
        tags=["Users"],
    ),
    retrieve=extend_schema(
        summary="Retrieve a user",
        description="Get details of a specific user by ID.",
        responses={200: UserSerializer},
        tags=["Users"],
    ),
)
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
