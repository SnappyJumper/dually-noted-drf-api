from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Extends the built-in User model with additional profile information.
    Each User has a one-to-one relationship with a UserProfile.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='images/',
        default='../default_profile_zx2qdz'
    )
    name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name}'s profile"


def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal receiver that creates a UserProfile automatically when a new User
    is created.
    """
    if created:
        UserProfile.objects.create(user=instance)


# Connect the post_save signal to the User model
post_save.connect(create_user_profile, sender=User)
