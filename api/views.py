from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import (
    CartItemSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
    ProductSerializer,
)
from catalog.cart import Cart
from catalog.models import Product


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.select_related("category")
    serializer_class = ProductSerializer
    filterset_fields = ["category"]

    def get_serializer_class(self):
        serializer = self.serializer_class
        if self.action == "list":
            serializer = ProductListSerializer
        elif self.action == "retrieve":
            serializer = ProductDetailSerializer
        return serializer


class CartViewSet(viewsets.ViewSet):
    def list(self, request):
        cart = Cart(request)
        serializer = CartItemSerializer(list(cart), many=True)
        return Response(
            {
                "item": serializer.data,
                "total_cost": cart.total_cost(),
                "count": len(cart),
            }
        )

    @action(detail=True, methods=["post"])
    def add(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        cart = Cart(request)
        cart.add(product)
        return Response({"status": "added", "product": product.name})

    @action(detail=True, methods=["post"])
    def increase(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        cart = Cart(request)
        cart.change_quantity(product, 1)
        return Response({"status": "increased", "product": product.name})

    @action(detail=True, methods=["post"])
    def decrease(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        cart = Cart(request)
        cart.change_quantity(product, -1)
        return Response({"status": "decreased", "product": product.name})

    @action(detail=True, methods=["post"])
    def remove(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        cart = Cart(request)
        cart.remove(product)
        return Response({"status": "removed", "product": product.name})
