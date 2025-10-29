from django.urls import path

from catalog.views import ProductListView

app_name = "products"

urlpatterns = [
    path("", ProductListView.as_view(), name="product-list"),
    path("category/<slug:slug>", ProductListView.as_view(), name="product_list_by_category"),
]
