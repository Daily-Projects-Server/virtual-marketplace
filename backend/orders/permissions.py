from rest_framework import permissions
from listings.models import Listing
from .models import Cart, CartItem


class IsNotAllowedToDestroy(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method != 'DELETE'


class IsItemAlreadyInCart(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == "create":
            listing_id = request.data.get("listing")
            if listing_id is None:
                return False
            listing = Listing.objects.get(id=listing_id)
            owner = listing.owner
            cart = Cart.objects.get(buyer=owner)
            return listing not in CartItem.objects.filter(cart=cart)

        return True
    
    #def has_object_permission(self, request, view, obj):
    #    if request.method == 'POST':
    #        listing = request.data.get('listing')
    #        if listing is None:
    #            return False
    #        print(f"Comparison: {obj.listing.id, listing}")
    #        return obj.listing.id != int(listing)
    #    return True
        