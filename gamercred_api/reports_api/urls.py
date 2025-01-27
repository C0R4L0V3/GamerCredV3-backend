from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ReportViewSet, get_reports_by_player


router = DefaultRouter()
router.register(r'incident', ReportViewSet, basename='reports')

urlpatterns = [
    path('', include(router.urls)),
    path('results/', get_reports_by_player, name='get_reports_by_player'),
]