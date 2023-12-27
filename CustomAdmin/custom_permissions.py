from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow users with is_admin=True to access the view.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
    
class IsSuperAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow users with is_superuser=True to access the view.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser