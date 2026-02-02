from rest_framework.routers import DefaultRouter

from core.views import SchoolViewSet

router = DefaultRouter()
router.register(r"schools", SchoolViewSet, basename="schools")

urlpatterns = router.urls
