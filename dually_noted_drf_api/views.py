from rest_framework.decorators import api_view
from rest_framework.response import Response


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
