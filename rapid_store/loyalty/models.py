from django.db import models
from django.conf import settings

class LoyaltyProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='loyalty')
    points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.email} - {self.points} puntos"

class LoyaltyTransaction(models.Model):
    profile = models.ForeignKey(LoyaltyProfile, on_delete=models.CASCADE, related_name='transactions')
    description = models.CharField(max_length=255)
    points_changed = models.IntegerField()  # positivos para ganar, negativos para redimir
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile.user.email}: {self.points_changed} pts - {self.description}"
