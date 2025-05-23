from rest_framework import routers
from posts.views import PostViewSet

app_name = "posts"

router = routers.DefaultRouter()
router.register("posts", PostViewSet)
urlpatterns = router.urls
