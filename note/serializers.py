from rest_framework import serializers
from .models import Note, SharedNote, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['id', 'created_at']


class NoteSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), source='tags', many=True, write_only=True)

    class Meta:
        model = Note
        fields = ['id', 'user', 'content', 'created_at', 'updated_at',
                  'tags', 'tag_ids']
        read_only_fields = ['created_at', 'updated_at', 'user', 'id']


class SharedNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedNote
        fields = ['id', 'note', 'shared_with', 'permission', 'shared_at']
        read_only_fields = ['shared_at']
