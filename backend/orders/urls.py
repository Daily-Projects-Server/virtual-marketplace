from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"transactions", views.TransactionViewSet)
router.register(r"cart", views.CartViewSet)
router.register(r"cart-items", views.CartItemViewSet)
router.register(r"coupons", views.CouponViewSet)

urlpatterns = [
    path('', include(router.urls)),
]