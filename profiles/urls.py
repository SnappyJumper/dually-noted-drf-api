from django.urls import path
from profiles import views
from profiles.views import PublicProfileDetail

urlpatterns = [
    # Endpoint to list all profiles or create new ones
    path('profiles/', views.ProfileList.as_view()),

    # Endpoint to retrieve, update, or delete a specific profile by ID
    path('profiles/<int:pk>/', views.ProfileDetail.as_view()),

    # Public endpoint to retrieve a user profile by username
    path('profiles/username/<str:username>/', PublicProfileDetail.as_view()),
]
