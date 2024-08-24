from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code
        # Example of additional logging or customization
        if isinstance(exc, ValidationError):
            response.data['error_message'] = 'There was an issue with the data you provided.'
    
    return response
