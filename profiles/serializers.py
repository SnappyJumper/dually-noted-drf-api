from rest_framework import serializers

from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserProfile model.
    Includes the related username and a flag to indicate ownership.
    """
    user = serializers.ReadOnlyField(
        source='user.username'
    )  # Read-only username from related User
    # Indicates if the current user owns this profile
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        """
        Returns True if the currently authenticated user is the owner
        of the profile instance being serialized.
        """
        request = self.context.get('request')
        return request.user == obj.user

    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'profile_picture', 'name', 'bio',
            'created_at', 'is_owner'
        ]
