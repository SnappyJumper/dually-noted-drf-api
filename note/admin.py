from django.contrib import admin
from .models import Note, Tag, SharedNote

# Register your models with the Django admin site.
# This allows them to be managed through the Django admin interface.

admin.site.register(Note)        # admin panel
admin.site.register(Tag)         # panel
admin.site.register(SharedNote)  # admin panel
