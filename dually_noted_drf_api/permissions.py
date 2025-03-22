from rest_framework import permissions


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
    - Edit only if there permission is 'edit'.
    Owner of the note can always view and modify.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user

        is_owner = obj.note.user == user
        is_shared_user = obj.shared_with == user

        if is_owner:
            return True

        if request.method in permissions.SAFE_METHODS and is_shared_user:
            return True

        if (
            request.method not in permissions.SAFE_METHODS
            and is_shared_user
            and obj.permission == 'edit'
        ):
            return True

        return False
