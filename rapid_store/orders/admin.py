from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    """
    Permite ver los artículos del pedido directamente en la vista del pedido.
    """
    model = OrderItem
    extra = 0 # No mostrar formularios extra vacíos
    readonly_fields = ('product', 'quantity', 'unit_price', 'total_price')
    can_delete = False # No permitir borrar items desde el admin de la orden

    def has_add_permission(self, request, obj=None):
        return False # No permitir añadir items desde el admin de la orden


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Configuración personalizada para el modelo Order en el admin de Django.
    """
    list_display = (
        'id', 
        'user_email',
        'status',
        'created_at_formatted',
        'total'
    )
    search_fields = ('user__email', 'id')
    list_filter = ('status', 'created_at')
    inlines = [OrderItemInline]
    
    # Campos que no se podrán editar directamente en el formulario de detalle
    readonly_fields = ('user', 'created_at', 'total') 
    
    # Permite cambiar el estado directamente desde la lista de pedidos
    list_editable = ('status',)

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Usuario (Email)'

    def created_at_formatted(self, obj):
        return obj.created_at.strftime('%d-%m-%Y %H:%M')
    created_at_formatted.short_description = "Fecha de Creación"

    def get_queryset(self, request):
        # Optimiza la consulta para mejorar el rendimiento del admin
        return super().get_queryset(request).select_related('user').prefetch_related('items__product')