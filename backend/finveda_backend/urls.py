from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

def health_check(request):
    return JsonResponse({"status": "ok", "environment": "cloud"}, status=200)

urlpatterns = [
    path('', health_check),
    path('admin/', admin.site.urls),
    path('api/v1/', include('companies.urls')),
    
    # Schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
