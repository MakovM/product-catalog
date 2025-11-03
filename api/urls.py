from rest_framework import routers

from api.views import CartViewSet, ProductViewSet

app_name = "api_products"

router = routers.DefaultRouter()
router.register("products", ProductViewSet)
router.register("cart", CartViewSet, basename="cart")

urlpatterns = router.urls
