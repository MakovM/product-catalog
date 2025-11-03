from django.test import TestCase

from accounts.models import User
from catalog.models import Category, Product, Cart, CartItem


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


class CartModelTests(TestCase):
    def test_cart_creation_and_str(self):
        user = User.objects.create_user(username='testuser', password='12345')
        cart = Cart.objects.create(user=user)
        self.assertEqual(str(cart), f"Cart for user: {user.username} (ID: {cart.id})")

    def test_cart_item_creation_and_str(self):
        user = User.objects.create_user(username='testuser', password='12345')
        cart = Cart.objects.create(user=user)
        category = Category.objects.create(name="Tablets")
        product = Product.objects.create(
            name="Tablet Lenovo", category=category, price=123.50, stock=1
        )
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=1)
        self.assertEqual(str(cart_item),  f"{cart_item.quantity}x {product.name} in Cart {cart.id}")
