from django.contrib import admin
from .models import InventoryItem, InventoryLog

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'last_updated')
    search_fields = ('product__name',)

@admin.register(InventoryLog)
class InventoryLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'inventory_item', 'change', 'description', 'timestamp')
    search_fields = ('inventory_item__product__name', 'description')