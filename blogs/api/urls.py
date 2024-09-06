from rest_framework import routers

from api import views as api_views

router = routers.DefaultRouter()

router.register(r"posts", api_views.BlogPostViewSet, basename="posts")

urlpatterns = []

urlpatterns += router.urls
