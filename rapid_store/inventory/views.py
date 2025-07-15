from rest_framework import generics, permissions
from .models import InventoryItem, InventoryLog
from .serializers import InventoryItemSerializer, InventoryLogSerializer

class InventoryItemListView(generics.ListAPIView):
    """
    Vista para listar todos los items del inventario.
    """
    # CORRECCIÓN 1: Se optimiza la consulta para mejorar el rendimiento,
    # cargando los datos de productos y categorías en una sola vez.
    queryset = InventoryItem.objects.select_related('product__category').order_by('product__name')
    
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAdminUser]
    
    # CORRECCIÓN 2: Se desactiva la paginación para que la API devuelva un array,
    # solucionando así el error en el frontend.
    pagination_class = None

class InventoryItemDetailView(generics.RetrieveAPIView):
    """
    Vista para ver el detalle de un solo item de inventario.
    """
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAdminUser]

class InventoryLogCreateView(generics.CreateAPIView):
    """
    Vista para crear un nuevo registro de movimiento en el inventario.
    """
    queryset = InventoryLog.objects.all()
    serializer_class = InventoryLogSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        # La lógica de actualización del stock se maneja automáticamente
        # por la señal 'post_save' en models.py.
        serializer.save()