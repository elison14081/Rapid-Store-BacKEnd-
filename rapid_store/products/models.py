from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Asegúrate de que esta ruta de importación sea correcta según tu estructura de proyecto
from inventory.models import InventoryItem 

# --- Modelos de Producto y Categoría (Sin cambios) ---

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# --- SEÑAL PARA CREAR INVENTARIO AUTOMÁTICAMENTE ---

@receiver(post_save, sender=Product)
def create_inventory_item_for_new_product(sender, instance, created, **kwargs):
    """
    Esta función se ejecuta automáticamente cada vez que se guarda un Producto.
    Si el producto es nuevo (created=True), le crea su item de inventario
    con una cantidad inicial de 0.
    """
    if created:
        InventoryItem.objects.create(product=instance, quantity=0)