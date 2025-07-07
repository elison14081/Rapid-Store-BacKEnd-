from rest_framework import serializers
from .models import Order, OrderItem
from users.serializers import UserSerializer  # Para mostrar info del usuario

class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializador para los artículos de un pedido.
    Solo necesita recibir el ID del producto y la cantidad.
    """
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'unit_price', 'total_price']
        # Los precios se calculan automáticamente en el modelo,
        # por lo que son de solo lectura en la API.
        read_only_fields = ['unit_price', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializador para crear y listar pedidos.
    Maneja la creación de la orden y sus artículos anidados.
    """
    # Usamos el serializador de items para mostrar los detalles
    items = OrderItemSerializer(many=True)
    # Mostramos los datos del usuario en la respuesta (solo lectura)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        # Usamos 'user' y 'total' para que coincida con el modelo corregido
        fields = ['id', 'user', 'created_at', 'total', 'items']
        # Estos campos se asignan automáticamente o son propiedades
        read_only_fields = ['user', 'created_at', 'total']

    def create(self, validated_data):
        """
        Crea un nuevo pedido y sus artículos correspondientes.
        """
        # Extraemos los datos de los artículos del payload
        items_data = validated_data.pop('items')

        # Obtenemos el usuario autenticado desde el contexto de la vista
        user = self.context['request'].user

        # Creamos el pedido y lo asociamos al usuario
        order = Order.objects.create(user=user)

        # Creamos cada artículo del pedido
        for item_data in items_data:
            OrderItem.objects.create(
                order=order,
                product=item_data['product'],
                quantity=item_data['quantity']
            )
            # No es necesario calcular precios aquí. El modelo OrderItem lo hace solo.

        # No es necesario guardar el total. La propiedad @property lo calcula.
        return order
