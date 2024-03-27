from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to allow owners of an object or admin users to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the request method is safe (HEAD, OPTIONS)

        if request.method in ['HEAD', 'OPTIONS']:
            return True
        return obj.user == request.user and request.user.is_authenticated
