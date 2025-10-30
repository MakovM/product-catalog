from django.contrib import admin

from catalog.models import Category, Product


@admin.register(Category)
class Category(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name", "price", "stock")
    prepopulated_fields = {"slug": ("name",)}
