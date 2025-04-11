from rest_framework import serializers
from .models import Note, SharedNote, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Tag name cannot be empty.")
        if Tag.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("This tag name already exists.")
        return value


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

    # ✅ Field-level validation
    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be blank.")
        return value

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Content cannot be blank.")
        return value

    class Meta:
        model = Note
        fields = [
            'id', 'user', 'title', 'content',
            'created_at', 'updated_at',
            'tags', 'tag_ids', 'is_owner'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class SharedNoteSerializer(serializers.ModelSerializer):
    note = serializers.PrimaryKeyRelatedField(queryset=Note.objects.all())
    shared_with_username = serializers.ReadOnlyField(
        source='shared_with.username'
    )
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return obj.note.user == request.user

    def validate(self, data):
        request = self.context.get("request")
        note = data.get("note")
        shared_with = data.get("shared_with")

        if note.user != request.user:
            raise serializers.ValidationError({
                "note": "You can only share notes that you own."
            })

        if note.sharednote_set.filter(shared_with=shared_with).exists():
            raise serializers.ValidationError({
                "shared_with": "This user already has access to the note."
            })

        if shared_with == request.user:
            raise serializers.ValidationError({
                "shared_with": "You cannot share a note with yourself."
            })

        return data

    class Meta:
        model = SharedNote
        fields = [
            'id', 'note', 'shared_with',
            'shared_with_username', 'permission', 'shared_at', 'is_owner'
        ]
        read_only_fields = ['id', 'shared_with_username', 'shared_at']


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
