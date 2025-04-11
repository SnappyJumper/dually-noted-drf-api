from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers


class CurrentUserSerializer(UserDetailsSerializer):
    """
    Extends the default dj-rest-auth UserDetailsSerializer to include
    additional read-only fields from the related user profile:
    - profile_id: the ID of the user's associated profile
    - profile_picture: URL to the user's profile picture
    """

    profile_id = serializers.ReadOnlyField(source='userprofile.id')
    profile_picture = serializers.ReadOnlyField(
        source='userprofile.profile_picture.url'
    )

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            'profile_id',
            'profile_picture',
        )
