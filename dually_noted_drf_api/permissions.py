from rest_framework import permissions

from note.models import SharedNote


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to allow read-only access to any request,
    but write access only to the object's owner.
    """

    def has_object_permission(self, request, view, obj):
        # Allow all safe methods (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the object
        return obj.user == request.user


class IsNoteOwner(permissions.BasePermission):
    """
    Allows access only to the owner of the note.
    Used to restrict detail view/edit/delete to the note creator.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class CanViewOrEditSharedNote(permissions.BasePermission):
    """
    Custom permission for SharedNote access:
    - Owners of the note have full access.
    - Shared users can view the note.
    - Shared users can edit only if permission is set to 'edit'.
    - Shared users can delete the share (remove access)
      regardless of permission.
    """

    def has_object_permission(self, request, view, obj):
        # Ensure we're working with a SharedNote object
        if not isinstance(obj, SharedNote):
            return False

        user = request.user
        is_owner = obj.note.user == user
        is_shared_user = obj.shared_with == user

        # Full access for the owner
        if is_owner:
            return True

        # Shared user can view if using a safe method (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS and is_shared_user:
            return True

        # Shared user can edit if they have 'edit' permission
        if (
            request.method in ["PUT", "PATCH"]
            and is_shared_user
            and obj.permission == "edit"
        ):
            return True

        # Shared user can delete (remove themselves from the share)
        if request.method == "DELETE" and is_shared_user:
            return True

        # Deny all other cases
        return False
