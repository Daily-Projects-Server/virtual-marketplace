import logging
from datetime import datetime

# from django.conf import settings
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from .serializers import LoginSerializer, RegisterSerializer
from core.common import responseMessages


logger = logging.getLogger('django')

__all__ = ['LoginView', 'RegisterView', 'RefreshTokenView']

@method_decorator(sensitive_post_parameters('password'), name="dispatch")
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
            response.set_cookie('refresh_token', str(refresh), httponly=True) 
            return response
        
        except APIException as exe:
            logger.error(str(exe), exc_info=True)
            raise APIException(exe.detail)
        

@method_decorator(sensitive_post_parameters('password', 'confirm_password'), name="dispatch")
class RegisterView(APIView):
    permission_classes = []
    authentication_classes = []
    
    def post(self, request, format=None):
        try:
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(created=datetime.now())

            RESPONSE_DATA = {
                'message': "User register successfully",
                'response': responseMessages.SUCCESS_RESPONSE_MESSAGE,
            }
            return Response(RESPONSE_DATA, status=status.HTTP_200_OK)
        
        except APIException as exe:
            logger.error(str(exe), exc_info=True)
            raise APIException(exe.detail)
            


class RefreshTokenView(TokenRefreshView):
    """ overriding default refresh token view
    """
    def post(self, request, *args, **kwargs):
        try:
            cookie = request.headers.get('Cookie')
            refresh_token = cookie.split('refresh_token=')[1]

            serializer = super().get_serializer(data={'refresh': refresh_token})
            try:
               serializer.is_valid(raise_exception=True)
            except TokenError as e:
                raise InvalidToken(e.args[0])

            RESPONSE_DATA = {
            'response': responseMessages.SUCCESS_RESPONSE_MESSAGE,
            'access_token': serializer.validated_data.get('access')
            }
            response = Response(RESPONSE_DATA, status=status.HTTP_200_OK)
            response.set_cookie('refresh_token', serializer.validated_data.get('refresh'), httponly=True) 
            return response
        
        except APIException as exe:
            logger.error(str(exe), exc_info=True)
            raise APIException(exe.detail)
    