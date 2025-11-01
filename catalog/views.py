from django.shortcuts import get_object_or_404, redirect
from django.views import generic

from catalog.cart.facade import Cart
from catalog.models import Category, Product


class ProductListView(generic.ListView):
    model = Product
    context_object_name = "product_list"
    template_name = "catalog/product_list.html"
    paginate_by = 8

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        if slug:
            return Product.objects.filter(category__slug=slug)
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = Category.objects.all()
        context["categories"] = categories

        context["current_category_slug"] = self.kwargs.get("slug", "")

        return context


class ProductDetailView(generic.DetailView):
    model = Product
    context_object_name = "product"
    template_name = "catalog/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class CartDetailView(generic.TemplateView):
    template_name = "catalog/cart_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context["cart"] = cart
        context["categories"] = Category.objects.all()
        return context


class CartAddView(generic.View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product)
        return redirect("products:cart_detail")


class CartIncreaseView(generic.View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.change_quantity(product=product, delta=1)
        return redirect("products:cart_detail")


class CartDecreaseView(generic.View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.change_quantity(product=product, delta=-1)
        return redirect("products:cart_detail")


class CartRemoveView(generic.View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product=product)
        return redirect("products:cart_detail")
