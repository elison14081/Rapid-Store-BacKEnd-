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
        log = serializer.save()
        item = log.inventory_item
        item.quantity += log.change
        item.save()
