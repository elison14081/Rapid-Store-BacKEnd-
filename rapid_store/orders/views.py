from rest_framework import generics, permissions
from .models import Order
from .serializers import OrderSerializer

class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Se filtra por 'user' en lugar de 'client'.
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        # Se pasa el contexto de la solicitud (que incluye al usuario)
        # al serializador para que pueda usarlo en el método 'create'.
        serializer.save()
