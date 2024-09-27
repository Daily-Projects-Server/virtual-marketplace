from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# We only add tags to the views that are used in the API documentation.
# The code remains the same as the original implementation.


@extend_schema(
    summary="Login and return access and refresh tokens",
    tags=["Authentication"],
)
class TaggedTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(summary="Refresh access token", tags=["Authentication"])
class TaggedTokenRefreshView(TokenRefreshView):
    pass
