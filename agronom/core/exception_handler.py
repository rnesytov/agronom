from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None and getattr(exc, 'custom_code', None) is not None:
        response = {
            'code': exc.custom_code,
            'body': response
        }

    return response
