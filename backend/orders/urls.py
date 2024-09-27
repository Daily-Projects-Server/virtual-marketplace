from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import cart_item_views, cart_views, coupon_views, transaction_views

router = DefaultRouter()
router.register(r"transactions", transaction_views.TransactionViewSet)
router.register(r"cart", cart_views.CartViewSet)
router.register(r"cart-item", cart_item_views.CartItemViewSet, basename="cart-item")
router.register(r"coupons", coupon_views.CouponViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
