from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
# App views
from users.views import *
from listings.views import *
from orders.views import *

# Routers
router = routers.DefaultRouter()
# Users
router.register(r"users", UserViewSet)
router.register(r"addresses", AddressViewSet)
router.register(r"user-addresses", UserAddressViewSet)
router.register(r"favorites", FavoriteViewSet)
router.register(r"reviews", ReviewViewSet)
router.register(r"messages", MessageViewSet)
# Listings
router.register(r"listings", ListingViewSet)
router.register(r"categories", CategoryViewSet)
# Orders
router.register(r"transactions", TransactionViewSet)
router.register(r"cart", CartViewSet)
router.register(r"cart-items", CartItemViewSet)
router.register(r"coupons", CouponViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
