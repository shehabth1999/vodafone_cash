from rest_framework import permissions

class IS_STAFF(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff

class IS_HEADER(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.is_admin

class IS_ACTIVATE(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_activate

class IS_ADMIN(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin

class IS_SUPERUSER(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
    