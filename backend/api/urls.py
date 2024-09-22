from django.urls import path, include
from rest_framework import routers
# App views
from users.views import *
from listings.views import *
from orders.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Routers
router = routers.DefaultRouter()
# Users
router.register(r"users", UserViewSet)
router.register(r"addresses", AddressViewSet)
router.register(r"favorites", FavoriteViewSet, basename='favorite')
router.register(r"reviews", ReviewViewSet)
# # Listings
router.register(r"listings", ListingViewSet)
router.register(r"categories", CategoryViewSet)
# # Orders
router.register(r"transactions", TransactionViewSet)
router.register(r"cart", CartViewSet)
router.register(r"cart-item", CartItemViewSet)
router.register(r"coupons", CouponViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("", include('users.urls')),
    # path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh') # When the access token expires,
    # use the /token/refresh/ endpoint to provide a new access token.
]
