# Archivo: urls.py principal del proyecto (CORREGIDO)

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
from products.urls import router as api_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/users/', include('users.urls')),

    path('api/', include(api_router.urls)),

    path('api/orders/', include('orders.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/loyalty/', include('loyalty.urls')),
    path('api/inventory/', include('inventory.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)