from django.urls import path
from .views import OrderListCreateView, OrderDetailView, OrderUpdateStatusView

app_name = 'orders'

urlpatterns = [
    # URL para listar y crear pedidos: /api/orders/
    path('', OrderListCreateView.as_view(), name='order-list-create'),
    
    # URL para ver el detalle de un pedido: /api/orders/5/
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    
    # URL para que un admin actualice el estado: /api/orders/update-status/5/
    path('update-status/<int:pk>/', OrderUpdateStatusView.as_view(), name='order-update-status'),
]