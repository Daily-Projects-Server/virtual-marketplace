from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"listings", views.ListingViewSet)
router.register(r"categories", views.CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]