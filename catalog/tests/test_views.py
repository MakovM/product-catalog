from django.test import Client, TestCase
from django.urls import reverse

from catalog.models import Category, Product


class ProductListViewSet(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Tablets", slug="tablets")
        self.product = Product.objects.create(
            name="iPad",
            slug="ipad",
            price=599.99,
            category=self.category,
            description="Apple tablet",
        )

    def test_product_list_view(self):
        url = reverse("products:product-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "iPad")

    def test_product_detail_view(self):
        url = reverse("products:product_detail", args=[self.product.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)


class CartViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Tablets", slug="tablets")
        self.product = Product.objects.create(
            name="iPad",
            slug="ipad",
            price=599.99,
            category=self.category,
            stock=10,
        )
        self.second_product = Product.objects.create(
            name="Lenovo",
            slug="lenovo",
            price=765.66,
            category=self.category,
            stock=5,
        )

    def test_add_to_cart_view(self):
        response = self.client.post(
            reverse(
                "products:add_to_cart", kwargs={"product_id": self.product.id}
            )
        )
        self.assertEqual(response.status_code, 302)
        session = self.client.session
        cart_data = session.get("cart")
        self.assertIn(str(self.product.id), cart_data)
        self.assertEqual(cart_data[str(self.product.id)]["quantity"], 1)

    def test_remove_item_from_cart(self):
        self.client.post(
            reverse(
                "products:add_to_cart", kwargs={"product_id": self.product.id}
            )
        )
        self.client.post(
            reverse(
                "products:add_to_cart",
                kwargs={"product_id": self.second_product.id},
            )
        )

        response = self.client.post(
            reverse(
                "products:cart_remove", kwargs={"product_id": self.product.id}
            )
        )
        self.assertEqual(response.status_code, 302)
        session = self.client.session
        cart_data = session.get("cart")
        self.assertNotIn(str(self.product.id), cart_data)
        self.assertIn(str(self.second_product.id), cart_data)
        self.assertEqual(cart_data[str(self.second_product.id)]["quantity"], 1)

    def test_increase_and_decrease_item_quantity(self):

        self.client.post(
            reverse(
                "products:add_to_cart", kwargs={"product_id": self.product.id}
            )
        )
        self.client.post(
            reverse(
                "products:cart_increase",
                kwargs={"product_id": self.product.id},
            )
        )
        session = self.client.session
        cart_data = session.get("cart")
        self.assertIn(str(self.product.id), cart_data)
        self.assertEqual(cart_data[str(self.product.id)]["quantity"], 2)

        self.client.post(
            reverse(
                "products:cart_decrease",
                kwargs={"product_id": self.product.id},
            )
        )
        session = self.client.session
        cart_data = session.get("cart")
        self.assertEqual(cart_data[str(self.product.id)]["quantity"], 1)

    def test_cart_detail_view(self):
        self.client.post(
            reverse(
                "products:add_to_cart", kwargs={"product_id": self.product.id}
            )
        )
        response = self.client.get(reverse("products:cart_detail"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
