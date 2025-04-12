from django.db.models import Q
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from dually_noted_drf_api.permissions import (CanViewOrEditSharedNote,
                                              IsNoteOwner)

from .models import Note, SharedNote, Tag
from .serializers import (NoteSerializer, SharedNoteDetailSerializer,
                          SharedNoteSerializer, TagSerializer)


class NoteList(APIView):
    """
    Handles listing and creating notes for the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve all notes belonging to the authenticated user.
        """
        notes = Note.objects.filter(user=request.user)
        serializer = NoteSerializer(
            notes, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new note for the authenticated user.
        """
        serializer = NoteSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteDetail(APIView):
    """
    Handles retrieval, updating, and deletion of a specific note.
    Only the owner of the note is permitted to access these actions.
    """
    permission_classes = [IsNoteOwner]

    def get_object(self, pk):
        """
        Helper method to get the note instance and check ownership.
        """
        try:
            note = Note.objects.get(pk=pk)
            self.check_object_permissions(self.request, note)
            return note
        except Note.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Retrieve a specific note by its ID.
        """
        note = self.get_object(pk)
        serializer = NoteSerializer(note, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a specific note.
        """
        note = self.get_object(pk)
        serializer = NoteSerializer(
            note, data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a specific note.
        """
        note = self.get_object(pk)
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SharedNoteList(APIView):
    """
    Lists shared notes or allows the user to share a note.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Return notes that are either owned by the user or shared with them.
        """
        shared_notes = SharedNote.objects.filter(
            Q(note__user=request.user) | Q(shared_with=request.user)
        ).distinct()

        serializer = SharedNoteDetailSerializer(
            shared_notes, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request):
        """
        Share a note with another user. Only note owners can perform this.
        """
        serializer = SharedNoteSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            note = serializer.validated_data['note']

            if note.user != request.user:
                return Response(
                    {"detail": "You can only share notes that you own."},
                    status=status.HTTP_403_FORBIDDEN
                )

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SharedNoteDetail(APIView):
    """
    Handles retrieving, updating, and removing shared note access.
    Permissions are based on whether the user is the owner or a shared user.
    """
    permission_classes = [CanViewOrEditSharedNote]

    def get_object(self, pk):
        """
        Retrieve the shared note and verify user permissions.
        """
        try:
            shared_note = SharedNote.objects.select_related('note').get(pk=pk)
            self.check_object_permissions(self.request, shared_note)
            return shared_note
        except SharedNote.DoesNotExist:
            raise Http404("Shared note not found.")

    def get(self, request, pk):
        """
        Get a shared note's details.
        """
        shared_note = self.get_object(pk)
        serializer = SharedNoteDetailSerializer(
            shared_note, context={'request': request}
        )
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a shared note. Only allowed if permission is 'edit'.
        """
        shared_note = self.get_object(pk)

        if shared_note.permission != "edit":
            raise PermissionDenied(
                "You do not have permission to edit this note."
            )

        serializer = SharedNoteDetailSerializer(
            shared_note,
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()  # Custom update on nested note
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Remove access to a shared note.
        Only the recipient can remove themselves.
        """
        shared_note = self.get_object(pk)

        if shared_note.shared_with != request.user:
            return Response(
                {"detail": "You do not have permission to remove this note."},
                status=status.HTTP_403_FORBIDDEN
            )

        shared_note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagList(APIView):
    """
    Handles listing and creation of tags.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve a list of all available tags.
        """
        tags = Tag.objects.all()
        serializer = TagSerializer(
            tags, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new tag.
        """
        serializer = TagSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagDetail(APIView):
    """
    Handles retrieving, updating, and deleting a specific tag.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Retrieve a specific tag instance by primary key.
        """
        try:
            return Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Retrieve a specific tag's details.
        """
        tag = self.get_object(pk)
        serializer = TagSerializer(tag, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a specific tag.
        """
        tag = self.get_object(pk)
        serializer = TagSerializer(
            tag, data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a specific tag.
        """
        tag = self.get_object(pk)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
