from rest_framework import serializers
from .models import UserProfile
from note.models import SharedNote


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return request.user == obj.user

    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'profile_picture', 'name', 'bio',
            'created_at', 'is_owner'
        ]


class SharedNotePreviewSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="note.title")
    content = serializers.CharField(source="note.content")
    permission = serializers.CharField()

    class Meta:
        model = SharedNote
        fields = ["id", "title", "content", "permission"]


class PublicUserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    profile_picture = serializers.ImageField()
    shared_notes = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['username', 'name', 'bio', 'profile_picture', 'shared_notes']

    def get_shared_notes(self, obj):
        """
        Return notes shared by this profile's user with the requesting user.
        """
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return []

        shared_notes = SharedNote.objects.filter(
            note__user=obj.user,
            shared_with=request.user
        ).select_related('note')

        return SharedNotePreviewSerializer(shared_notes, many=True).data
