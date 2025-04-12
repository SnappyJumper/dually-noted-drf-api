from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    """
    Represents a keyword or label that can be associated with notes.
    Tags help organize and categorize content.
    """
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Note(models.Model):
    """
    Represents a personal note created by a user.
    Each note has a title, content, and optional tags.
    Notes are user-owned and timestamped.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notes'
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='notes'
    )

    def __str__(self):
        return self.title


class SharedNote(models.Model):
    """
    Represents a note that has been shared with another user.
    Includes permission level and sharing metadata.
    """
    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name='shared_notes'
    )
    shared_with = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shared_with_me'
    )

    permission_choices = [
        ('read', 'Read Only'),
        ('edit', 'Can Edit'),
    ]
    permission = models.CharField(
        max_length=10,
        choices=permission_choices,
        default='read'
    )
    shared_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.note.title} shared with {self.shared_with.username}"
