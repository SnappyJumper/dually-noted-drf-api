from django.urls import path
from note import views

urlpatterns = [
    # Notes
    path(
        'notes/',
        views.NoteList.as_view(),
        name='note-list'
    ),
    path(
        'notes/<int:pk>/',
        views.NoteDetail.as_view(),
        name='note-detail'
    ),

    # Shared Notes
    path(
        'shared-notes/',
        views.SharedNoteList.as_view(),
        name='shared-note-list',
    ),
    path(
        'shared-notes/<int:pk>/',
        views.SharedNoteDetail.as_view(),
        name='shared-note-detail',
    ),

    # Tags
    path(
        'tags/',
        views.TagList.as_view(),
        name='tag-list'
    ),
    path(
        'tags/<int:pk>/',
        views.TagDetail.as_view(),
        name='tag-detail'
    ),
]
