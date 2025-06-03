from django.urls import path
from .views import InventoryItemListView, InventoryItemDetailView, InventoryLogCreateView

urlpatterns = [
    path('', InventoryItemListView.as_view(), name='inventory-list'),
    path('<int:pk>/', InventoryItemDetailView.as_view(), name='inventory-detail'),
    path('log/', InventoryLogCreateView.as_view(), name='inventory-log'),
]
