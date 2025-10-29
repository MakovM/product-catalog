from django.contrib import admin

from catalog.models import Category, Product

@admin.register(Category)
class Category(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", )}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ("name", "description")
    list_display = ("name", "description", "price", "stock")
    prepopulated_fields = {"slug": ("name", )}
