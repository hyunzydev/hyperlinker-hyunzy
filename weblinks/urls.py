from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WebLinkViewSet,
    UserViewSet,
)  # ✅ views에서 WebLinkViewSet, UserViewSet 가져오기

router = DefaultRouter()
router.register(r"weblinks", WebLinkViewSet, basename="weblink")
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),  # ✅ DRF API 경로 추가
]
