from django.test import TestCase

from catalog.models import Category, Product


class CategoryModelTests(TestCase):
    def test_category_creation_and_str(self):
        category = Category.objects.create(name="Tablets")
        self.assertEqual(str(category), "Tablets")


class ProductModelTests(TestCase):
    def test_product_creation_and_str(self):
        category = Category.objects.create(name="Tablets")
        product = Product.objects.create(
            name="Tablet Lenovo", category=category, price=123.50, stock=1
        )
        self.assertEqual(str(product), "Tablet Lenovo")
