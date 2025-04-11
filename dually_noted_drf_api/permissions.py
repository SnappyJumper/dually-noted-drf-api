from rest_framework import permissions
from note.models import SharedNote


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsNoteOwner(permissions.BasePermission):
    """
    Allows access only to the note owner.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class CanViewOrEditSharedNote(permissions.BasePermission):
    """
    Shared user can:
    - View the shared note if they have permission.
    - Edit only if their permission is 'edit'.
    - Delete (remove themselves) regardless of permission.
    Owner of the note can always view and modify.
    """

    def has_object_permission(self, request, view, obj):
        if not isinstance(obj, SharedNote):
            return False

        user = request.user
        is_owner = obj.note.user == user
        is_shared_user = obj.shared_with == user

        if is_owner:
            return True

        if request.method in permissions.SAFE_METHODS and is_shared_user:
            return True

        if (
            request.method in ["PUT", "PATCH"]
            and is_shared_user
            and obj.permission == "edit"
        ):
            return True

        if request.method == "DELETE" and is_shared_user:
            return True

        return False
