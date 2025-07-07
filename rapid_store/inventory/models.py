from django.db import models
from products.models import Product
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class InventoryItem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='inventory')
    quantity = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} en stock"

class InventoryLog(models.Model):
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='logs')
    change = models.IntegerField()  # Puede ser positivo (ingreso) o negativo (salida)
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.inventory_item.product.name}: {self.change} unidades - {self.description}"

@receiver(post_save, sender=InventoryLog)
def update_inventory_quantity_on_save(sender, instance, created, **kwargs):
    if created:
        inventory_item = instance.inventory_item
        inventory_item.quantity += instance.change
        inventory_item.save()

@receiver(post_delete, sender=InventoryLog)
def update_inventory_quantity_on_delete(sender, instance, **kwargs):
    inventory_item = instance.inventory_item
    inventory_item.quantity -= instance.change
    inventory_item.save()
