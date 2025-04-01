from rest_framework.decorators import api_view
from rest_framework.response import Response
from .settings import (
    JWT_AUTH_COOKIE,
    JWT_AUTH_REFRESH_COOKIE,
    JWT_AUTH_SAMESITE,
    JWT_AUTH_SECURE
)


@api_view()
def root_route(request):
    """
    Root route for the API. Returns a list of available endpoints.
    """
    return Response({
        'profiles': '/api/profiles/',
        'notes': '/api/notes/',
        'shared_notes': '/api/shared_notes/',
        'tags': '/api/tags/',
        'auth': {
            'login': '/api/auth/login/',
            'logout': '/api/auth/logout/',
            'register': '/api/auth/register/',
            'password_reset': '/api/auth/password/reset/',
            'password_change': '/api/auth/password/change/'
        }
    })

# dj_rest_auth logout view fix
@api_view(['POST'])
def logout_route(request):
    response = Response()
    response.set_cookie(
        key=JWT_AUTH_COOKIE,
        value='',
        httponly=True,
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        max_age=0,
        samesite=JWT_AUTH_SAMESITE,
        secure=JWT_AUTH_SECURE,
    )
    response.set_cookie(
        key=JWT_AUTH_REFRESH_COOKIE,
        value='',
        httponly=True,
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        max_age=0,
        samesite=JWT_AUTH_SAMESITE,
        secure=JWT_AUTH_SECURE,
    )
    return response
