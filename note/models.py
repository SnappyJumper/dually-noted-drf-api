from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='notes')
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='notes')

    def __str__(self):
        return self.title


class SharedNote(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE,
                             related_name='shared_notes')
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name='shared_with_me')

    permission_choices = [
        ('read', 'Read Only'),
        ('edit', 'Can Edit'),
    ]
    permission = models.CharField(max_length=10, choices=permission_choices,
                                  default='read')
    shared_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.note.title} shared with {self.shared_with.username}"
