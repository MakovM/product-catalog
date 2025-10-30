from decimal import Decimal

from django.conf import settings

from catalog.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def save(self):
        self.session.modified = True

    def add(self, product):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 1,
                "price": str(product.price),
            }
        else:
            self.cart[product_id]["quantity"] += 1
        self.save()

    def change_quantity(self, product, delta=1):
        product_id = str(product.id)
        if product_id in self.cart:
            current_quantity = self.cart[product_id]["quantity"]
            new_quantity = current_quantity + delta

            if new_quantity < 1:
                return

            self.cart[product_id]["quantity"] = min(
                new_quantity, product.stock
            )
            self.save()

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart_copy = self.cart.copy()
        for product in products:
            cart_copy[str(product.id)]["product"] = product
        for item in cart_copy.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def total_cost(self):
        return sum(
            Decimal(item["price"]) * item["quantity"]
            for item in self.cart.values()
        )
