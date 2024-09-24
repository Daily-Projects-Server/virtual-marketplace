from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from .auth_views import TaggedTokenObtainPairView, TaggedTokenRefreshView


urlpatterns = [
    path('api/', include([
        path('', include('users.urls')),
        path('', include('listings.urls')),
        path('', include('orders.urls')),
        path('token/', TaggedTokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('token/refresh/', TaggedTokenRefreshView.as_view(), name='token_refresh'),
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ])),
]