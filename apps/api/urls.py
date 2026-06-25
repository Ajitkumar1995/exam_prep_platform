from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AuthViewSet,
    ExamCategoryViewSet,
    ExamViewSet,
    MockTestViewSet,
    AnalyticsViewSet,
)

router = DefaultRouter()
router.register(r"auth", AuthViewSet, basename="auth")
router.register(r"exam-categories", ExamCategoryViewSet, basename="exam-categories")
router.register(r"exams", ExamViewSet, basename="exams")
router.register(r"mock-tests", MockTestViewSet, basename="mock-tests")
router.register(r"analytics", AnalyticsViewSet, basename="analytics")

urlpatterns = [
    path("", include(router.urls)),
]
