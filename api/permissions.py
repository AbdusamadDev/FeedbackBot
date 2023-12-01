from rest_framework import permissions


# Custom permission classes
class IsSuperAdmin(permissions.BasePermission):
    """
    Allows access only to super admin users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Allows write permissions only to admin users, read-only for others.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
