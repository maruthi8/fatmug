from rest_framework.routers import DefaultRouter

from api.views import VideoViewSet

router = DefaultRouter(trailing_slash=False)

router.register("videos", VideoViewSet, basename="videos")

urlpatterns = router.urls
