from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, SectorViewSet, IngestViewSet

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'sectors', SectorViewSet)
router.register(r'ingest', IngestViewSet, basename='ingest')

urlpatterns = [
    path('', include(router.urls)),
]
