from rest_framework import generics, permissions
from .models import Order
from .serializers import OrderSerializer
from users.permissions import IsAdminUser # Asumiendo que este es tu permiso de admin

# Permiso personalizado para asegurar que solo el dueño del pedido pueda verlo
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

# --- Vistas de la API ---

class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Si el usuario es admin, muestra todos los pedidos; si no, solo los suyos.
        if self.request.user.is_staff or self.request.user.is_admin:
            return Order.objects.all().order_by('-created_at')
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        # CORRECCIÓN: La vista ahora solo guarda el serializador.
        # El serializador se encargará de asignar el usuario desde el contexto.
        serializer.save()

class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = Order.objects.all()

class OrderUpdateStatusView(generics.UpdateAPIView):
    serializer_class = OrderSerializer
    # Asumo que tu permiso se llama IsAdminUser, ajústalo si es necesario
    permission_classes = [permissions.IsAuthenticated, IsAdminUser] 
    queryset = Order.objects.all()
    http_method_names = ['patch']