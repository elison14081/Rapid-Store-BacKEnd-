from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from loyalty.models import LoyaltyProfile

# Manager personalizado para el modelo de usuario
class CustomUserManager(BaseUserManager):
    # Método para crear un usuario normal
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')  # Valida que el email sea obligatorio
        email = self.normalize_email(email)  
        user = self.model(email=email, name=name, **extra_fields)  
        user.set_password(password)  
        user.save(using=self._db)  
        return user

    # Método para crear un superusuario (admin)
    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)  
        extra_fields.setdefault('is_staff', True)  
        extra_fields.setdefault('is_superuser', True)  
        return self.create_user(email, name, password, **extra_fields)  

# Modelo personalizado de usuario
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)  # Email único para cada usuario
    name = models.CharField(max_length=255)  # Nombre del usuario
    is_client = models.BooleanField(default=True)  # Indica si es cliente
    is_admin = models.BooleanField(default=False)  # Indica si es admin
    is_staff = models.BooleanField(default=False)  # Indica si es staff (permite acceso al admin de Django)
    is_active = models.BooleanField(default=True)  # Indica si la cuenta está activa
    date_joined = models.DateTimeField(auto_now_add=True)  # Fecha de registro

    objects = CustomUserManager()  # Asigna el manager personalizado

    USERNAME_FIELD = 'email'  # Campo usado para login
    REQUIRED_FIELDS = ['name']  # Campos requeridos además del email

    def __str__(self):
        return self.email  # Representación en texto del usuario

# Señal que crea un perfil de lealtad automáticamente al crear un usuario
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_loyalty_profile(sender, instance, created, **kwargs):
    if created:
        LoyaltyProfile.objects.get_or_create(user=instance)  # Crea el perfil de lealtad si no existe

