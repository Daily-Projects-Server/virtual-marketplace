import logging

from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer, RegisterSerializer
from core.common import responseMessages


logger = logging.getLogger('django')

__all__ = ['LoginView', 'RegisterView']

class LoginView(APIView):
    permission_classes = []
    authentication_classes = []
    
    def post(self, request, format=None):
        try:
            serializer = LoginSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data.get('user')
            refresh = RefreshToken.for_user(user)
            
            RESPONSE_DATA = { 
                'message': responseMessages.LOGIN_MESSAGE ,
                'response': responseMessages.SUCCESS_RESPONSE_MESSAGE,
                'access_token': str(refresh.access_token) 
             }
            response = Response(RESPONSE_DATA, status=status.HTTP_200_OK)
            # storing the refresh token in the http only cookie
            response.set_cookie('refresh_token', str(refresh), httponly=True) 
            return response
        
        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            raise APIException(exe)
        


class RegisterView(APIView):
    permission_classes = []
    authentication_classes = []
    
    def post(self, request, format=None):
        try:
            serializer = RegisterSerializer(data=request.data, instance=settings.AUTH_USER_MODEL)
            serializer.is_valid(raise_exception=True)

            RESPONSE_DATA = {
                'message': "User register successfully",
                'response': responseMessages.SUCCESS_RESPONSE_MESSAGE,
            }
            return Response(RESPONSE_DATA, status=status.HTTP_200_OK)
        
        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            raise APIException(exe)
            
    