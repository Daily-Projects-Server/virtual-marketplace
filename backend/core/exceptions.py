import logging

from rest_framework import status
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
    ValidationError,
)
from rest_framework.views import exception_handler
from rest_framework_simplejwt.exceptions import InvalidToken

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    # Call the default exception handler to get the standard error response
    response = exception_handler(exc, context)

    # Log the exception for debugging
    if response is not None:
        logger.error(f"Exception occurred: {exc}")

        # Customize responses based on status codes
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            response.data = {
                "error": "Unauthorized access",
                "message": (
                    "Your access token has expired or is invalid. "
                    "Please login again or refresh the token."
                ),
            }
        elif response.status_code == status.HTTP_403_FORBIDDEN:
            response.data = {
                "error": "Forbidden",
                "message": "You do not have permission to access this resource.",
            }
        elif response.status_code == status.HTTP_400_BAD_REQUEST:
            response.data = {
                "error": "Bad Request",
                "message": "There was a problem with your request.",
            }
        elif isinstance(exc, ValidationError):
            response.data = {
                "error": "Validation Error",
                "message": "There was an issue with the data you provided.",
            }
        elif isinstance(exc, AuthenticationFailed):
            response.data = {
                "error": "Authentication Failed",
                "message": (
                    "Authentication failed. " "Please provide valid credentials."
                ),
            }
        elif isinstance(exc, NotAuthenticated):
            response.data = {
                "error": "Not Authenticated",
                "message": "You are not authenticated. Please log in.",
            }
        elif isinstance(exc, InvalidToken):
            response.data = {
                "error": "Invalid Token",
                "message": (
                    "The provided token is invalid or expired. "
                    "Please refresh the token or log in again."
                ),
            }

    return response
