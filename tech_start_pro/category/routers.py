from rest_framework.routers import SimpleRouter

from .api import CategoryViewSet

app_name = "category"
main_router = SimpleRouter()

main_router.register(r"category", CategoryViewSet, basename="category")

urlpatterns = main_router.urls
