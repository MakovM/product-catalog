from django.core.files.storage import default_storage
from django.db import models
from django.templatetags.static import static


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True,
        default="static/img/img.png",
    )
    description = models.TextField(blank=True)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-available", "name"]

    @property
    def image_url(self):
        if self.image and default_storage.exists(self.image.name):
            return self.image.url
        return static("img/img.png")

    def save(self, *args, **kwargs):
        self.available = self.stock > 0
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
