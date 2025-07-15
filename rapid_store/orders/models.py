from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

# Importa los modelos de tus otras aplicaciones
from products.models import Product
from loyalty.models import LoyaltyProfile
from inventory.models import InventoryLog, InventoryItem
from notifications.models import Notification

# --- Modelos de la App ---

class Order(models.Model):
    """
    Representa un pedido realizado por un usuario, con su estado y total.
    """
    # Opciones para el estado del pedido
    STATUS_CHOICES = (
        ('pending', 'Pendiente'),
        ('processing', 'En Proceso'),
        ('shipped', 'Enviado'),
        ('delivered', 'Entregado'),
        ('canceled', 'Cancelado'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    @property
    def total(self):
        """
        Calcula el costo total del pedido sumando el precio de todos sus artículos.
        """
        # Usamos un generador para un mejor rendimiento en pedidos grandes
        return sum(item.total_price for item in self.items.all())

    def __str__(self):
        return f"Order #{self.id} by {self.user.email} - {self.get_status_display()}"


class OrderItem(models.Model):
    """
    Representa un artículo específico dentro de un pedido.
    """
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    def clean(self):
        """
        Validación a nivel de modelo. Aunque la validación principal está en el
        serializador, es buena práctica tenerla aquí también para el admin de Django.
        """
        if self.product.inventory.quantity < self.quantity:
            raise ValidationError(f"No hay suficiente stock para {self.product.name}. Disponible: {self.product.inventory.quantity}")

    def save(self, *args, **kwargs):
        """
        Asigna el precio del producto y calcula el precio total antes de guardar.
        """
        if not self.pk: # Solo al crear el objeto por primera vez
            self.unit_price = self.product.price
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"


# --- Señales de Django para Automatizaciones ---

@receiver(post_save, sender=OrderItem)
def update_inventory_on_order_item_creation(sender, instance, created, **kwargs):
    """
    Cuando se crea un nuevo OrderItem, esta señal crea un registro en InventoryLog
    para documentar la venta. La app 'inventory' se encargará de actualizar el stock.
    """
    if created:
        try:
            # 1. Obtenemos el objeto de inventario relacionado con el producto.
            inventory_item = instance.product.inventory

            # 2. Creamos un log para registrar la salida de stock.
            #    La señal en 'inventory/models.py' se activará al crear este log
            #    y será la que actualice la cantidad final del inventario.
            InventoryLog.objects.create(
                inventory_item=inventory_item,
                change=-instance.quantity,  # El cambio es negativo porque es una venta
                description=f"Venta en pedido #{instance.order.id}"
            )
        except InventoryItem.DoesNotExist:
            # Esta excepción se daría si un producto vendido no tiene un
            # registro de inventario, lo cual sería un problema de datos.
            print(f"ALERTA CRÍTICA: El producto {instance.product.name} (ID: {instance.product.id}) no tiene un inventario asociado.")


@receiver(pre_save, sender=Order)
def notify_user_on_status_change(sender, instance, **kwargs):
    """
    Envía una notificación al usuario cuando el estado de su pedido cambia.
    """
    if instance.pk: # Solo se ejecuta si el objeto ya existe en la BD
        try:
            old_instance = Order.objects.get(pk=instance.pk)
            # Si el estado ha cambiado, crea una notificación
            if old_instance.status != instance.status:
                Notification.objects.create(
                    user=instance.user,
                    title=f"Actualización de tu pedido #{instance.id}",
                    message=f"El estado de tu pedido ha cambiado a: {instance.get_status_display()}."
                )
        except Order.DoesNotExist:
            pass # El objeto es nuevo, no se hace nada

@receiver(post_save, sender=Order)
def add_loyalty_points_on_order(sender, instance, created, **kwargs):
    """
    Asigna puntos de lealtad al usuario cuando se crea el pedido.
    """
    if created:
        # Asegurarse de que el total se calcula después de que los items se han guardado.
        # Puede ser necesario recalcularlo si los items se añaden después.
        order_total = instance.total
        # Calcula los puntos (ej: 1 punto por cada sol de compra)
        points_earned = int(order_total)

        if points_earned > 0:
            profile, _ = LoyaltyProfile.objects.get_or_create(user=instance.user)
            profile.points += points_earned
            profile.save()
