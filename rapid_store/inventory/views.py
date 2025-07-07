from rest_framework import generics, permissions
from .models import InventoryItem, InventoryLog
from .serializers import InventoryItemSerializer, InventoryLogSerializer
from rest_framework.permissions import IsAdminUser

class InventoryItemListView(generics.ListAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAdminUser]

class InventoryItemDetailView(generics.RetrieveAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAdminUser]

class InventoryLogCreateView(generics.CreateAPIView):
    queryset = InventoryLog.objects.all()
    serializer_class = InventoryLogSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        # La lógica de actualización de cantidad se ha eliminado.
        # La señal 'post_save' en models.py se encargará automáticamente.
        serializer.save()
