from rest_framework.routers import SimpleRouter

from product.api import ProductViewSet

app_name = "product"
main_router = SimpleRouter()

main_router.register(r"product", ProductViewSet, basename="product")

urlpatterns = main_router.urls
