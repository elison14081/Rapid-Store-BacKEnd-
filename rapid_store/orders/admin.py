from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'user_id',
        'created_at_formatted',  # Usa el método personalizado
        'product_quantities', 
        'product_unit_prices', 
        'total'
    )
    search_fields = ('user__email',)
    list_filter = ('created_at',)
    inlines = [OrderItemInline]

    def user_id(self, obj):
        return obj.user.id
    user_id.short_description = "Usuario (ID)"

    def created_at_formatted(self, obj):
        return obj.created_at.strftime('%d-%m-%y')
    created_at_formatted.short_description = "Creado en"

    def product_quantities(self, obj):
        return ", ".join([str(item.quantity) for item in obj.items.all()])
    product_quantities.short_description = "Cantidad del producto"

    def product_unit_prices(self, obj):
        return ", ".join([str(item.unit_price) for item in obj.items.all()])
    product_unit_prices.short_description = "Precio unitario"