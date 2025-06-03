from django.db import models
from products.models import Product
from users.models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from loyalty.models import LoyaltyProfile
from django.conf import settings

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        return sum(item.total_price for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.unit_price = self.product.price
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)

@receiver(post_save, sender=Order)
def add_loyalty_points_on_order(sender, instance, created, **kwargs):
    if created:
        total = instance.total  # Total gastado en la orden
        points = int(total // 10) * 100  # 100 puntos por cada 10 soles
        try:
            profile = LoyaltyProfile.objects.get(user=instance.user)
            profile.points += points
            profile.save()
        except LoyaltyProfile.DoesNotExist:
            pass  # O crea el perfil si no existe

@receiver(post_save, sender=OrderItem)
def update_loyalty_points_on_orderitem(sender, instance, **kwargs):
    order = instance.order
    total = order.total
    points = int(total // 10) * 100  # 100 puntos por cada 10 soles
    try:
        profile = LoyaltyProfile.objects.get(user=order.user)
        profile.points = points
        profile.save()
    except LoyaltyProfile.DoesNotExist:
        pass

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_loyalty_profile(sender, instance, created, **kwargs):
    if created:
        LoyaltyProfile.objects.get_or_create(user=instance)
