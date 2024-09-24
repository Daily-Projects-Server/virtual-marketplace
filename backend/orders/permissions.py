from rest_framework import permissions
from listings.models import Listing
from .models import Cart, CartItem


class IsNotAllowedToDestroy(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method != 'DELETE'


class IsNotItemAlreadyInCart(permissions.BasePermission):
    def does_item_exist(self, request, *items):
        for item in items:
            if item is None:
                return False
        return True

    def has_permission(self, request, view):
        if view.action == "create":
            # Retrieve the listing and cart IDs from the request data
            listing_id = request.data.get("listing")
            cart_id = request.data.get("cart")
            if not self.does_item_exist(listing_id, cart_id):
                return False
            
            # Retrieve the listing and cart objects
            listing = Listing.objects.get(id=listing_id)
            cart = Cart.objects.get(id=cart_id)

            # Check if the item is already in the cart
            return not CartItem.objects.filter(cart=cart, listing=listing).exists()
        
        return True
    
    #def has_object_permission(self, request, view, obj):
    #    if request.method == 'POST':
    #        listing = request.data.get('listing')
    #        if listing is None:
    #            return False
    #        print(f"Comparison: {obj.listing.id, listing}")
    #        return obj.listing.id != int(listing)
    #    return True
        