from rest_framework import permissions


class IsItselfOrReadOnly(permissions.BasePermission):
    """Permission to only allow a user to edit itself"""

    def has_object_permission(self, request, view, obj):
        # all read permissions are still allowed
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user


class IsItself(permissions.BasePermission):
    """User must be the request's user"""

    def has_object_permission(self, request, view, obj):
        return obj == request.user
