from rest_framework import permissions


class IsNotAllowedToDestroy(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method != 'DELETE'


class IsItemAlreadyInCart(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            listing = request.data.get('listing')
            if listing is None:
                return False
            return not obj.listing.id == int(listing)
        return True
        