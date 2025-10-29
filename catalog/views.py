from django.shortcuts import render
from django.views import generic

from catalog.models import Category, Product


class ProductListView(generic.ListView):
    model = Product
    context_object_name = "product_list"
    template_name = "catalog/product_list.html"

    def get_queryset(self):
        return Product.objects.all()
