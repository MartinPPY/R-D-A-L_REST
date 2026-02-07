from django.contrib import admin
from django.urls import path,include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema')),
    path('api/v1/auth/',include('authentication.urls')),
    path('api/v1/core/',include('core.urls')),
    
]
