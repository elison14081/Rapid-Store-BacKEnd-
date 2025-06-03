from rest_framework import serializers
from .models import InventoryItem, InventoryLog
from products.serializers import ProductSerializer

class InventoryLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryLog
        fields = ['id', 'change', 'description', 'timestamp']

class InventoryItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    logs = InventoryLogSerializer(many=True, read_only=True)

    class Meta:
        model = InventoryItem
        fields = ['id', 'product', 'quantity', 'last_updated', 'logs']
