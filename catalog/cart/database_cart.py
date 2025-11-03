from catalog.models import Cart, CartItem


class DatabaseCart:
    def __init__(self, user):
        self.user = user
        self.cart, _ = Cart.objects.get_or_create(user=user)
        self._items_cache = None

    def _load_items(self):
        if self._items_cache is None:
            self._items_cache = list(self.cart.items.select_related("product"))

    def add(self, product, quantity=1):
        item, created = CartItem.objects.get_or_create(
            cart=self.cart, product=product
        )
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.quantity = min(item.quantity, product.stock)
        item.save()

    def change_quantity(self, product, delta=1):
        try:
            item = CartItem.objects.get(cart=self.cart, product=product)
            new_quantity = item.quantity + delta
            if new_quantity < 1:
                return
            else:
                item.quantity = min(new_quantity, product.stock)
                item.save()
            self._items_cache = None
        except CartItem.DoesNotExist:
            pass

    def __iter__(self):
        self._load_items()
        for item in self._items_cache:
            item.price = item.product.price
            yield item

    def __len__(self):
        self._load_items()
        return sum(item.quantity for item in self._items_cache)

    def remove(self, product):
        CartItem.objects.filter(cart=self.cart, product=product).delete()
        self._items_cache = None

    def total_cost(self):
        self._load_items()
        return sum(
            item.total_price for item in self._items_cache
        )
