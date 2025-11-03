from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from api.serializers import ProductListSerializer, ProductDetailSerializer
from catalog.models import Category, Product
from rest_framework.test import APIClient


PRODUCTS_URL = reverse("api_products:product-list")

CART_URL = reverse("api_products:cart-list")


def product_detail_url(product_id):
    return reverse("api_products:product-detail", args=[product_id])


def sample_category(**params):
    defaults = {"name": "Monitors", "slug": "monitors"}
    defaults.update(params)

    return Category.objects.create(**defaults)


def sample_product(**params):
    category, _ = Category.objects.get_or_create(
        name="Tablets", slug="tablets"
    )
    defaults = {
        "name": "iPad",
        "slug": "ipad",
        "price": 599.99,
        "category": category,
        "description": "Apple tablet",
        "stock": 10,
    }
    defaults.update(params)

    return Product.objects.create(**defaults)


class CatalogApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = sample_category()
        self.product = sample_product()
        self.second_product = sample_product(
            name="Samsung",
            slug="samsung",
            price=2765.66,
            category=self.category,
            stock=10,
        )

    def test_api_product_list(self):
        products = Product.objects.all()
        serializer = ProductListSerializer(products, many=True)
        res = self.client.get(PRODUCTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_api_product_detail(self):
        url = product_detail_url(self.product.id)
        res = self.client.get(url)

        serializer = ProductDetailSerializer(self.product)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_api_filter_products_list_by_category(self):
        res = self.client.get(PRODUCTS_URL, {"category": self.category.id})
        serializer_first_product = ProductListSerializer(self.product)
        serializer_second_product = ProductListSerializer(self.second_product)

        self.assertNotIn(serializer_first_product.data, res.data["results"])
        self.assertIn(serializer_second_product.data, res.data["results"])

    def test_add_to_cart(self):
        url = reverse("api_products:cart-add", kwargs={"pk": self.product.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        session_cart = self.client.session["cart"]
        self.assertIn(str(self.product.id), session_cart)
        self.assertEqual(session_cart[str(self.product.id)]["quantity"], 1)

    def test_increase_and_decrease_product_quantity(self):
        url = reverse("api_products:cart-add", kwargs={"pk": self.product.id})
        self.client.post(url)

        url = reverse(
            "api_products:cart-increase", kwargs={"pk": self.product.id}
        )

        self.client.post(url)
        session_cart = self.client.session["cart"]
        self.assertIn(str(self.product.id), session_cart)
        self.assertEqual(session_cart[str(self.product.id)]["quantity"], 2)

        url = reverse(
            "api_products:cart-decrease", kwargs={"pk": self.product.id}
        )
        self.client.post(url)
        self.client.session.save()
        session_cart = self.client.session["cart"]

        self.assertIn(str(self.product.id), session_cart)
        self.assertEqual(session_cart[str(self.product.id)]["quantity"], 1)

    def test_remove_product_from_cart(self):
        url = reverse("api_products:cart-add", kwargs={"pk": self.product.id})
        self.client.post(url)
        url = reverse(
            "api_products:cart-add", kwargs={"pk": self.second_product.id}
        )
        self.client.post(url)

        url = reverse(
            "api_products:cart-remove", kwargs={"pk": self.product.id}
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        session_cart = self.client.session["cart"]
        self.assertIn(str(self.second_product.id), session_cart)
        self.assertNotIn(str(self.product.id), session_cart)
