from rest_framework import serializers
from .models import InventoryItem, InventoryLog
from products.models import Product, Category

# --- SERIALIZADORES AUXILIARES (Definidos aquí para claridad y control) ---

# 1. Un serializador simple para la categoría.
class CategoryForProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

# 2. Un serializador para el producto que usa el serializador de categoría.
class ProductForInventorySerializer(serializers.ModelSerializer):
    category = CategoryForProductSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'image', 'category']

# --- SERIALIZADORES PRINCIPALES ---

# 3. El serializador de logs, con el campo 'inventory_item' para permitir la creación.
class InventoryLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryLog
        fields = ['id', 'inventory_item', 'change', 'description', 'timestamp']

# 4. El serializador principal de inventario, que usa los serializadores auxiliares.
class InventoryItemSerializer(serializers.ModelSerializer):
    product = ProductForInventorySerializer(read_only=True)
    logs = InventoryLogSerializer(many=True, read_only=True)

    class Meta:
        model = InventoryItem
        fields = ['id', 'product', 'quantity', 'last_updated', 'logs']