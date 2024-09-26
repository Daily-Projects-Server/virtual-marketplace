import logging
from datetime import datetime


from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from django.conf import settings
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from ..serializers import LoginSerializer, RegisterSerializer
from core.common import responseMessages
from core.common.globalFunctions import get_refresh_token

logger = logging.getLogger("django")

__all__ = ["LoginView", "RegisterView", "RefreshTokenView"]


@method_decorator(sensitive_post_parameters("password"), name="dispatch")
@extend_schema(
    summary="Login",
    description="Login a user.",
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Successful login response",
            examples=[
                OpenApiExample(
                    "Successful Response",
                    value={
                        "message": "User logged in successfully",
                        "response": "OK",
                        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                    },
                    status_codes=["200"],
                ),
            ],
        ),
        400: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Bad request response",
            examples=[
                OpenApiExample(
                    "Bad Request",
                    value={
                        "email": ["This field is required."],
                        "password": ["This field is required."],
                    },
                    status_codes=["400"],
                ),
            ],
        ),
        401: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Unauthorized response",
            examples=[
                OpenApiExample(
                    "Unauthorized",
                    value={
                        "detail": "No active account found with the given credentials"
                    },
                    status_codes=["401"],
                ),
            ],
        ),
    },
    tags=["Authentication"],
)
class LoginView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request, format=None):
        try:
            serializer = LoginSerializer(
                data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user = serializer.validated_data.get("user")
            refresh = RefreshToken.for_user(user)

            response_data = {
                "message": responseMessages.LOGIN_MESSAGE,
                "response": responseMessages.SUCCESS_RESPONSE_MESSAGE,
                "access_token": str(refresh.access_token),
            }
            response = Response(response_data, status=status.HTTP_200_OK)
            response.set_cookie(
                "refresh_token",
                str(refresh),
                httponly=True,
                secure=True,
                samesite="Lax",
            )
            return response

        except APIException as exe:
            logger.error(str(exe), exc_info=True)
            return Response(
                {"detail": "An internal error has occurred. Please try again later."},
                status=status.HTTP_400_BAD_REQUEST,
            )


@method_decorator(
    sensitive_post_parameters("password", "confirm_password"), name="dispatch"
)
@extend_schema(
    summary="Register",
    description="Register a new user.",
    request=RegisterSerializer,
    responses={
        201: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Successful registration response",
            examples=[
                OpenApiExample(
                    "Successful Response",
                    value={
                        "message": "User registered successfully",
                        "response": "Ok",
                    },
                    status_codes=["201"],
                ),
            ],
        ),
        400: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Bad request response",
            examples=[
                OpenApiExample(
                    "Missing Information",
                    value={
                        "first_name": ["This field is required."],
                        "last_name": ["This field is required."],
                        "email": ["This field is required."],
                        "password": ["This field is required."],
                        "confirm_password": ["This field is required."],
                    },
                    status_codes=["400"],
                ),
                OpenApiExample(
                    "User Already Exists",
                    value={"email": ["User with this email already exists."]},
                    status_codes=["400"],
                ),
            ],
        ),
    },
    tags=["Authentication"],
)
class RegisterView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save(created=datetime.now())

            response_data = {
                "message": "User registered successfully",
                "response": responseMessages.SUCCESS_RESPONSE_MESSAGE,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        except serializers.ValidationError as e:
            if "email" in e.detail and any(
                "unique" in str(error).lower() for error in e.detail["email"]
            ):
                return Response(
                    {"email": ["User with this email already exists."]},
                    status=status.HTTP_409_CONFLICT,
                )
            else:
                response_data = e.detail
            response_status = status.HTTP_400_BAD_REQUEST

        return Response(response_data, status=response_status)


@extend_schema(
    summary="Refresh Token",
    description="Refresh the access token using the refresh token.",
    responses={
        200: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Successful token refresh response",
            examples=[
                OpenApiExample(
                    "Successful Response",
                    value={
                        "response": "OK",
                        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                    },
                    status_codes=["200"],
                ),
            ],
        ),
        401: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Unauthorized response",
            examples=[
                OpenApiExample(
                    "Unauthorized",
                    value={
                        "detail": "Token is invalid or expired",
                        "code": "token_not_valid",
                    },
                    status_codes=["401"],
                ),
            ],
        ),
    },
    tags=["Authentication"],
)
class RefreshTokenView(TokenRefreshView):
    """overriding default refresh token view"""

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = get_refresh_token(request)
            serializer = super().get_serializer(data={"refresh": refresh_token})

            try:
                serializer.is_valid(raise_exception=True)
            except TokenError as e:
                raise InvalidToken(e.args[0])

            RESPONSE_DATA = {
                "response": responseMessages.SUCCESS_RESPONSE_MESSAGE,
                "access_token": serializer.validated_data.get("access"),
            }
            response = Response(RESPONSE_DATA, status=status.HTTP_200_OK)
            response.set_cookie(
                "refresh_token",
                serializer.validated_data.get("refresh"),
                httponly=True,
                secure=True,
            )
            return response

        except APIException as exe:
            logger.error(str(exe), exc_info=True)
            return Response(
                {"detail": "An internal error has occurred."},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Logout",
        description="Logout the authenticated user by blacklisting their refresh token.",
        tags=["Authentication"],
        request=OpenApiTypes.NONE,  # No request body needed
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Successful logout response",
                examples=[
                    OpenApiExample(
                        "Successful Response",
                        value={"detail": "User logged out successfully."},
                        status_codes=["200"],
                    ),
                ],
            ),
            400: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Bad request response",
                examples=[
                    OpenApiExample(
                        "Error Response",
                        value={"detail": "Error message"},
                        status_codes=["400"],
                    ),
                ],
            ),
        },
    )
    def post(self, request):
        try:
            token = get_refresh_token(request)
            old_refresh = RefreshToken(token)
            old_refresh.blacklist()
            # TODO: delete refresh token from cookie
            return Response(
                {"detail": "User logged out successfully."}, status=status.HTTP_200_OK
            )

        except APIException as exe:
            logger.error(str(exe), exc_info=True)
            raise APIException("An internal error has occurred.")
