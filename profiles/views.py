from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from dually_noted_drf_api.permissions import IsOwnerOrReadOnly

from .models import UserProfile
from .serializers import UserProfileSerializer


class ProfileList(APIView):
    """
    Handles listing all user profiles.
    """

    def get(self, request):
        profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(
            profiles, many=True, context={'request': request}
        )
        return Response(serializer.data)


class ProfileDetail(APIView):
    """
    Retrieve, update, or delete a specific user profile by ID.
    Only the owner of the profile has permission to update it.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pk):
        """
        Helper method to retrieve the profile instance by primary key.
        Raises 404 if not found or permission is denied.
        """
        try:
            profile = UserProfile.objects.get(pk=pk)
            self.check_object_permissions(self.request, profile)
            return profile
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Returns the profile data for the given ID.
        """
        profile = self.get_object(pk)
        serializer = UserProfileSerializer(
            profile, context={'request': request}
        )
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Updates the profile with data provided by the owner.
        """
        profile = self.get_object(pk)
        serializer = UserProfileSerializer(
            profile, data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublicProfileDetail(APIView):
    """
    Read-only view of a user's profile by username.
    This is primarily used to show user info when viewing shared notes.
    """

    def get_object(self, username):
        """
        Fetches the profile for the given username.
        Raises 404 if not found.
        """
        try:
            return UserProfile.objects.select_related('user') \
                .get(user__username=username)
        except UserProfile.DoesNotExist:
            raise Http404("User profile not found.")

    def get(self, request, username):
        """
        Returns the profile data for the given username.
        """
        profile = self.get_object(username)
        serializer = UserProfileSerializer(
            profile, context={'request': request}
        )
        return Response(serializer.data)
