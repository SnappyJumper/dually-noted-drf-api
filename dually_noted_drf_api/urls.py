"""dually_noted_drf_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from .views import logout_route, root_route

urlpatterns = [

    # Root route
    path('', root_route),

    # Admin
    path('admin/', admin.site.urls),

    # Django Rest Framework browsable API authentication
    path('api-auth/', include('rest_framework.urls')),

    # Logout route
    path('dj-rest-auth/logout/', logout_route),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),

    # Profile
    path('', include('profiles.urls')),

    # Note
    path('', include('note.urls')),

    # Auth
    path('dj-rest-auth/', include('dj_rest_auth.urls')),

    # Allauth
    path(
        'dj-rest-auth/registration/',
        include('dj_rest_auth.registration.urls')
    ),
]
