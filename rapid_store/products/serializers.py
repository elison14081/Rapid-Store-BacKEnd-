from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    
    # --- ESTA LÍNEA ES LA CLAVE ---
    # Devuelve la cantidad del inventario asociado. 
    # El 'default=0' maneja productos sin inventario creado.
    inventory_quantity = serializers.IntegerField(source='inventory.quantity', read_only=True, default=0)

    class Meta:
        model = Product
        # --- ASEGÚRATE DE QUE 'inventory_quantity' ESTÉ EN LA LISTA ---
        fields = [
            'id', 
            'name', 
            'description', 
            'price', 
            'category', 
            'category_id', 
            'image', 
            'inventory_quantity', 
            'created_at'
        ]