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
    Root route for the API.

    Returns a dictionary of key API endpoints to help developers
    understand how to access major parts of the application.
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


@api_view(['POST'])
def logout_route(request):
    """
    Custom logout route for JWT-based authentication.

    This function manually clears the authentication and refresh
    cookies by setting them to an empty value and expiring them.

    It's useful for clients that rely on cookie-based auth instead of tokens
    in headers, particularly in browser environments.
    """
    response = Response()

    # Clear the access token cookie
    response.set_cookie(
        key=JWT_AUTH_COOKIE,
        value='',
        httponly=True,
        expires='Thu, 01 Jan 1970 00:00:00 GMT',  # Expire immediately
        max_age=0,
        samesite=JWT_AUTH_SAMESITE,
        secure=JWT_AUTH_SECURE,
    )

    # Clear the refresh token cookie
    response.set_cookie(
        key=JWT_AUTH_REFRESH_COOKIE,
        value='',
        httponly=True,
        expires='Thu, 01 Jan 1970 00:00:00 GMT',  # Expire immediately
        max_age=0,
        samesite=JWT_AUTH_SAMESITE,
        secure=JWT_AUTH_SECURE,
    )

    return response
