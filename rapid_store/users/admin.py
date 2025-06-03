from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'name', 'is_admin', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'name')
    list_filter = ('is_admin', 'is_active', 'is_staff', 'is_superuser')