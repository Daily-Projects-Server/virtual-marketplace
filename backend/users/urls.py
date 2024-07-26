
from django.urls import path

from . import auth_views

urlpatterns = [
   path('login/', auth_views.LoginView.as_view(), name="login"),
   path('register/', auth_views.RegisterView.as_view(), name="register"),
]
