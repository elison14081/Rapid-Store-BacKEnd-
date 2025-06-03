from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'client', 'created_at', 'total_price', 'items']
        read_only_fields = ['client', 'created_at', 'total_price']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        client = self.context['request'].user
        order = Order.objects.create(client=client, total_price=0)
        total = 0

        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            price = product.price * quantity
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)
            total += price

        order.total_price = total
        order.save()
        return order
