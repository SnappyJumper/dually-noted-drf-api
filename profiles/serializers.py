from rest_framework import serializers
from .models import UserProfile


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
