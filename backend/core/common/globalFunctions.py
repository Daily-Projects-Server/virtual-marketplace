from rest_framework import status
from rest_framework.response import Response

from core.common import responseMessages


# common functions
def get_refresh_token(request):
    cookie = request.headers.get("Cookie")
    refresh_token = cookie.split("refresh_token=")[1]
    return refresh_token


def handle_success_response(data, message):
    if data:
        response_data = {
            "message": message,
            "data": data,
            "response": responseMessages.SUCCESS_RESPONSE_MESSAGE,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    response_data = {
        "message": message,
        "response": responseMessages.SUCCESS_RESPONSE_MESSAGE,
    }
    return Response(response_data, status=status.HTTP_200_OK)
