from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError # Importante para enviar un error 400

class InventoryItem(models.Model):
    product = models.OneToOneField('products.Product', on_delete=models.CASCADE, related_name='inventory')
    quantity = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} en stock"

class InventoryLog(models.Model):
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='logs')
    change = models.IntegerField()
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.inventory_item.product.name}: {self.change} unidades - {self.description}"

# --- SEÑALES CON VALIDACIÓN DE STOCK ---

@receiver(post_save, sender=InventoryLog)
def update_inventory_quantity_on_save(sender, instance, created, **kwargs):
    if created:
        inventory_item = instance.inventory_item
        current_quantity = inventory_item.quantity or 0
        new_quantity = current_quantity + instance.change

        # CORRECCIÓN: Verificamos si el stock resultante sería negativo
        if new_quantity < 0:
            # Si es negativo, lanzamos un error de validación claro.
            # DRF lo convertirá en un error 400 (Bad Request) para el frontend.
            raise ValidationError(
                f"No hay suficiente stock para '{inventory_item.product.name}'. "
                f"Stock actual: {current_quantity}, se intentó restar: {abs(instance.change)}."
            )

        inventory_item.quantity = new_quantity
        inventory_item.save()

@receiver(post_delete, sender=InventoryLog)
def update_inventory_quantity_on_delete(sender, instance, **kwargs):
    # Esta señal revierte el cambio si se elimina un log de inventario
    inventory_item = instance.inventory_item
    current_quantity = inventory_item.quantity or 0
    
    # Aquí también validamos para evitar inconsistencias
    new_quantity = current_quantity - instance.change
    if new_quantity < 0:
      # En el caso improbable de que revertir un log cree un negativo, lo dejamos en 0.
      new_quantity = 0

    inventory_item.quantity = new_quantity
    inventory_item.save()