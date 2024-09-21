from rest_framework import permissions


class IsNotAllowedToDestroy(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method != 'DELETE'
