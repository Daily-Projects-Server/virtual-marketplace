from rest_framework import permissions
from listings.models import Listing
from .models import Cart, CartItem


class IsNotAllowedToDestroy(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method != 'DELETE'


class IsNotItemAlreadyInCart(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == "create":
            listing_id = request.data.get("listing")
            cart_id = request.data.get("cart")
            if listing_id is None or cart_id is None:
                return False
            listing = Listing.objects.get(id=listing_id)
            cart = Cart.objects.get(id=cart_id)
            return not CartItem.objects.filter(cart=cart, listing=listing).exists()
        
        return True
        