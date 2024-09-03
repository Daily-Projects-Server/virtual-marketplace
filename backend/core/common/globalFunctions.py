from rest_framework.response import Response
from rest_framework import status

from core.common import responseMessages

# common functions
def get_refresh_token(request):
     cookie = request.headers.get('Cookie')
     refresh_token = cookie.split('refresh_token=')[1]
     return refresh_token


def handle_success_response(data ,message):
    if data:
         RESPONSE_DATA = {
                'message': message,
                'data': data,
                'response': responseMessages.SUCCESS_RESPONSE_MESSAGE,
            }
         return Response(RESPONSE_DATA, status=status.HTTP_200_OK)


    RESPONSE_DATA = {
                'message': message,
                'response': responseMessages.SUCCESS_RESPONSE_MESSAGE,
            }
    return Response(RESPONSE_DATA, status=status.HTTP_200_OK)
