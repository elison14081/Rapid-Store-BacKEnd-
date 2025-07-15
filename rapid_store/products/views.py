from rest_framework import viewsets, permissions
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.parsers import MultiPartParser, FormParser
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # GET, HEAD, OPTIONS permitidos para todos
        return request.user and request.user.is_authenticated and request.user.is_admin

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        """
        Filtra los productos por categoría si se proporciona el parámetro 'category' en la URL.
        """
        queryset = Product.objects.all().order_by('name')
        category_id = self.request.query_params.get('category')
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        return queryset
