from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import auth_views, address_views, review_views, user_views

router = DefaultRouter()
router.register(r"users", user_views.UserViewSet)
router.register(r"addresses", address_views.AddressViewSet)
router.register(r"reviews", review_views.ReviewViewSet, basename='review')  

urlpatterns = [
    path('', include(router.urls)),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('register/', auth_views.RegisterView.as_view(), name="register"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
