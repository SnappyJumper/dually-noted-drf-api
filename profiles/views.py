from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserProfile
from .serializers import UserProfileSerializer
from dually_noted_drf_api.permissions import IsOwnerOrReadOnly
from .serializers import PublicUserProfileSerializer


class ProfileList(APIView):
    def get(self, request):
        profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(
            profiles, many=True, context={'request': request})
        return Response(serializer.data)


class ProfileDetail(APIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            profile = UserProfile.objects.get(pk=pk)
            self.check_object_permissions(self.request, profile)
            return profile
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        profile = self.get_object(pk)
        serializer = UserProfileSerializer(
            profile, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        profile = self.get_object(pk)
        print("Uploaded file:", request.FILES.get('image'))
        serializer = UserProfileSerializer(
            profile, data=request.data, context={'request': request}
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PublicProfileDetail(APIView):
    def get_object(self, username):
        try:
            return UserProfile.objects.select_related('user') \
                .get(user__username=username)
        except UserProfile.DoesNotExist:
            raise Http404("User profile not found.")

    def get(self, request, username):
        profile = self.get_object(username)
        serializer = PublicUserProfileSerializer(  # ⬅️ use the new serializer
            profile, context={'request': request}
        )
        return Response(serializer.data)
