from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .models import Note, SharedNote, Tag
from .serializers import NoteSerializer, SharedNoteSerializer, TagSerializer
from dually_noted_drf_api.permissions import (
    IsNoteOwner, CanViewOrEditSharedNote
)


class NoteList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notes = Note.objects.filter(user=request.user)
        serializer = NoteSerializer(
            notes, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = NoteSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteDetail(APIView):
    permission_classes = [IsNoteOwner]

    def get_object(self, pk):
        try:
            note = Note.objects.get(pk=pk)
            self.check_object_permissions(self.request, note)
            return note
        except Note.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        note = self.get_object(pk)
        serializer = NoteSerializer(note, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        note = self.get_object(pk)
        serializer = NoteSerializer(
            note, data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        note = self.get_object(pk)
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SharedNoteList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        shared_notes = SharedNote.objects.filter(
            Q(note__user=request.user) | Q(shared_with=request.user)
        ).distinct()
        serializer = SharedNoteSerializer(
            shared_notes, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request):
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
    permission_classes = [CanViewOrEditSharedNote]

    def get_object(self, pk):
        try:
            shared_note = SharedNote.objects.get(pk=pk)
            self.check_object_permissions(self.request, shared_note)
        except SharedNote.DoesNotExist:
            raise Http404

        return shared_note

    def get(self, request, pk):
        shared_note = self.get_object(pk)
        note = shared_note.note

        serializer = NoteSerializer(note, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        shared_note = self.get_object(pk)
        note = shared_note.note

        # Ensure the user has 'edit' permission
        if (
            shared_note.shared_with != request.user
            or shared_note.permission != 'edit'
        ):
            raise PermissionDenied(
                "You do not have permission to edit this note."
            )

        serializer = NoteSerializer(
            note, data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        shared_note = self.get_object(pk)
        shared_note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(
            tags, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = TagSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        tag = self.get_object(pk)
        serializer = TagSerializer(tag, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        tag = self.get_object(pk)
        serializer = TagSerializer(
            tag, data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        tag = self.get_object(pk)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
