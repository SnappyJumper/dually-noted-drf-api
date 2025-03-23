from rest_framework import serializers
from .models import Note, SharedNote, Tag


class TagSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        # No ownership tracking, so always False (or you can omit this field)
        return False

    class Meta:
        model = Tag
        fields = ['id', 'name', 'created_at', 'is_owner']
        read_only_fields = ['id', 'created_at']


class NoteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    is_owner = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        write_only=True,
        source='tags'
    )

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return request.user == obj.user

    class Meta:
        model = Note
        fields = [
            'id', 'user', 'title', 'content',
            'created_at', 'updated_at',
            'tags', 'tag_ids', 'is_owner'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class SharedNoteSerializer(serializers.ModelSerializer):
    note_title = serializers.ReadOnlyField(source='note.title')
    shared_with_username = serializers.ReadOnlyField(source='shared_with.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return obj.note.user == request.user

    class Meta:
        model = SharedNote
        fields = [
            'id', 'note', 'note_title',
            'shared_with', 'shared_with_username',
            'permission', 'shared_at', 'is_owner'
        ]
        read_only_fields = ['id', 'note_title', 'shared_with_username', 'shared_at']