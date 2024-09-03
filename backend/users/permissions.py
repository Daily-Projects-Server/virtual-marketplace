from rest_framework import permissions
from listings.models import Listing


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsNotListingOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            return Listing.objects.get(pk=obj.listing.id).user != request.user
        return True
