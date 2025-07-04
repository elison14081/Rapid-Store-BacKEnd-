from django.db import models
from users.models import CustomUser  # Asegúrate que la app "users" esté registrada en INSTALLED_APPS

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)  # Nuevo campo
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name