from django.shortcuts import render
from django.views import generic

from catalog.models import Category, Product


class ProductListView(generic.ListView):
    model = Product
    context_object_name = "product_list"
    template_name = "catalog/product_list.html"

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        if slug:
            return Product.objects.filter(category__slug=slug)
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = Category.objects.all()
        context['categories'] = categories

        context['current_category_slug'] = None

        return context