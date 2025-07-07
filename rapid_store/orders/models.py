from django.db import models
from products.models import Product
from users.models import CustomUser  # Asegúrate que esta es la ruta a tu modelo de usuario
from django.db.models.signals import post_save
from django.dispatch import receiver
from loyalty.models import LoyaltyProfile

# --- Modelos de la App ---

class Order(models.Model):
    """
    Representa un pedido realizado por un usuario.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        """
        Calcula el costo total del pedido sumando el precio total de todos sus artículos.
        Esta propiedad es de solo lectura y se calcula dinámicamente.
        """
        return sum(item.total_price for item in self.items.all())

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    """
    Representa un artículo específico dentro de un pedido.
    """
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    # Los precios se guardan al momento de la compra para mantener un registro histórico
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        """
        Asigna el precio del producto y calcula el precio total antes de guardar.
        """
        if not self.pk: # Solo al crear el objeto
            self.unit_price = self.product.price
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"


# --- Señales de Django ---

@receiver(post_save, sender=Order)
def add_loyalty_points_on_order(sender, instance, created, **kwargs):
    """
    Asigna puntos de lealtad al usuario una sola vez, cuando el pedido se crea.
    """
    if created:
        # Se calcula el total usando la propiedad del modelo
        order_total = instance.total
        # Se otorgan 100 puntos por cada 10 soles gastados
        points_earned = int(order_total // 10) * 100

        if points_earned > 0:
            # Se usa get_or_create para seguridad, aunque el perfil ya debería existir
            profile, _ = LoyaltyProfile.objects.get_or_create(user=instance.user)
            profile.points += points_earned
            profile.save()