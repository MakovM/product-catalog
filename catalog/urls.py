from django.urls import path

from catalog.views import (CartAddView, CartDecreaseView, CartDetailView,
                           CartIncreaseView, CartRemoveView, ProductDetailView,
                           ProductListView)

app_name = "products"

urlpatterns = [
    path("", ProductListView.as_view(), name="product-list"),
    path(
        "category/<slug:slug>/",
        ProductListView.as_view(),
        name="product_list_by_category",
    ),
    path(
        "product/<slug:slug>/",
        ProductDetailView.as_view(),
        name="product_detail",
    ),
    path("cart/", CartDetailView.as_view(), name="cart_detail"),
    path(
        "cart/add/<int:product_id>/", CartAddView.as_view(), name="add_to_cart"
    ),
    path(
        "cart/remove/<int:product_id>/",
        CartRemoveView.as_view(),
        name="cart_remove",
    ),
    path(
        "cart/increase/<int:product_id>/",
        CartIncreaseView.as_view(),
        name="cart_increase",
    ),
    path(
        "cart/decrease/<int:product_id>/",
        CartDecreaseView.as_view(),
        name="cart_decrease",
    ),
]
