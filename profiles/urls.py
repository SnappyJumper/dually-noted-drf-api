from django.urls import path
from profiles import views
from profiles.views import PublicProfileDetail

urlpatterns = [
    path('profiles/', views.ProfileList.as_view()),
    path('profiles/<int:pk>/', views.ProfileDetail.as_view()),
    path('profiles/username/<str:username>/', PublicProfileDetail.as_view()),
]
