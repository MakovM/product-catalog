from django.urls import path

from catalog.views import ProductListView

app_name = "products"

urlpatterns = [path("", ProductListView.as_view(), name="product-list")]
