from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SleepDiagnosisViewSet

router = DefaultRouter()
router.register(r'diagnosis', SleepDiagnosisViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
