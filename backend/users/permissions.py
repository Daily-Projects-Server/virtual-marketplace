from rest_framework import permissions
from listings.models import Listing


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsAllowedToReview(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            listing_id = request.data.get('listing')
            if listing_id:
                listing = Listing.objects.get(pk=listing_id)
                return listing.owner != request.user
        return True

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update', 'destroy']:
            return obj.listing.owner != request.user
        return True


class IsAllowedToDestroyReview(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user