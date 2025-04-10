from rest_framework import serializers
from .models import Note, SharedNote, Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name', 'created_at']
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
    note = NoteSerializer(read_only=True)
    shared_with_username = serializers.ReadOnlyField(
        source='shared_with.username'
    )
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return obj.note.user == request.user

    class Meta:
        model = SharedNote
        fields = [
            'id', 'note', 'note',
            'shared_with', 'shared_with_username',
            'permission', 'shared_at', 'is_owner'
        ]
        read_only_fields = [
            'id', 'note', 'shared_with_username', 'shared_at'
        ]


class SharedNoteDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="note.title")
    content = serializers.CharField(source="note.content")
    permission = serializers.CharField(read_only=True)
    is_owner = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source="note.user.username")

    def get_is_owner(self, obj):
        request = self.context.get("request")
        return obj.note.user == request.user

    def update(self, instance, validated_data):
        # request = self.context.get("request")

        if instance.permission != "edit":
            raise serializers.ValidationError(
                "You do not have permission to edit this note."
            )

        note_data = validated_data.get("note", {})
        instance.note.title = note_data.get("title", instance.note.title)
        instance.note.content = note_data.get("content", instance.note.content)
        instance.note.save()
        return instance

    class Meta:
        model = SharedNote
        fields = ["id", "title", "content", "user", "permission", "is_owner"]
