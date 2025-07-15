# orders/serializers.py

from django.db import transaction
from rest_framework import serializers
from .models import Order, OrderItem
from users.serializers import UserSerializer
from products.models import Product
from products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializador para los artículos individuales dentro de un pedido.
    """
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['product_id', 'product', 'quantity', 'unit_price', 'total_price']
        read_only_fields = ['product', 'unit_price', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializador principal para crear y ver pedidos.
    """
    items = OrderItemSerializer(many=True)
    user = UserSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'status', 'status_display', 'total', 'items']
        read_only_fields = ['id', 'user', 'created_at', 'total', 'status_display']

    def validate_items(self, items_data):
        """
        Valida que haya artículos y que haya suficiente stock para cada uno
        antes de intentar crear el pedido.
        """
        if not items_data:
            raise serializers.ValidationError("El pedido debe tener al menos un artículo.")

        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            
            # --- CORRECCIÓN APLICADA AQUÍ ---
            # Se accede al stock a través de la relación 'inventory' definida en los modelos.
            # Por ejemplo: product.inventory.quantity
            if product.inventory.quantity < quantity:
                raise serializers.ValidationError(
                    f"Stock insuficiente para '{product.name}'. "
                    f"Disponible: {product.inventory.quantity}, solicitado: {quantity}."
                )
        return items_data

    @transaction.atomic
    def create(self, validated_data):
        """
        Crea la orden y sus artículos correspondientes dentro de una transacción
        atómica para garantizar la integridad de los datos.
        """
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        
        # 1. Se crea la orden principal
        order = Order.objects.create(user=user, **validated_data)

        # 2. Se crean los artículos del pedido
        for item_data in items_data:
            OrderItem.objects.create(
                order=order,
                product=item_data['product'],
                quantity=item_data['quantity']
            )
        
        # 3. Las señales 'post_save' que definimos en models.py se dispararán
        #    automáticamente aquí para actualizar el inventario.

        return order
