from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, auth_views

router = DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"addresses", views.AddressViewSet)
router.register(r"favorites", views.FavoriteViewSet, basename='favorite')
router.register(r"reviews", views.ReviewViewSet, basename='review')  

urlpatterns = [
    path('', include(router.urls)),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('register/', auth_views.RegisterView.as_view(), name="register"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
