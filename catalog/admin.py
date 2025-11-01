from django.contrib import admin

from catalog.models import Cart, CartItem, Category, Product


@admin.register(Category)
class Category(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name", "price", "stock")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product__name", "quantity")
