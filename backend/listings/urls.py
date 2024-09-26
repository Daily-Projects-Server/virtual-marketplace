from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import category_views, favorite_views, listing_views

router = DefaultRouter()
router.register(r"listings", listing_views.ListingViewSet)
router.register(r"categories", category_views.CategoryViewSet)
router.register(r"favorites", favorite_views.FavoriteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]