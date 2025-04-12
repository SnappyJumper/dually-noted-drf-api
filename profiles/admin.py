"""
Admin configuration for the user profile model.
Registers the UserProfile model to be manageable via the Django admin site.
"""

from django.contrib import admin

from .models import UserProfile

admin.site.register(UserProfile)
