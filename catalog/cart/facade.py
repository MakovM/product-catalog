from catalog.cart.database_cart import DatabaseCart
from catalog.cart.session_cart import SessionCart


class Cart:
    def __init__(self, request):
        self.request = request
        if request.user.is_authenticated:
            self.cart = DatabaseCart(request.user)
        else:
            self.cart = SessionCart(request)

    def __getattr__(self, item):
        return getattr(self.cart, item)

    def __len__(self):
        return len(self.cart)

    def __iter__(self):
        return iter(self.cart)
