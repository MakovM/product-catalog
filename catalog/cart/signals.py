from catalog.cart.database_cart import DatabaseCart
from catalog.cart.session_cart import SessionCart
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in


@receiver(user_logged_in)
def merge_cart_after_login(sender, request, user, **kwargs):
    session_cart = SessionCart(request)
    db_cart = DatabaseCart(user)

    for item in session_cart:
        product = item["product"]
        quantity = item["quantity"]

        db_cart.add(product, quantity)
    session_cart.cart.clear()
    session_cart.save()
