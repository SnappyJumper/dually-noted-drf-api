from django.contrib import admin
from .models import Note, Tag, SharedNote

admin.site.register(Note)
admin.site.register(Tag)
admin.site.register(SharedNote)
