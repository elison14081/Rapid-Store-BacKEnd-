# users/permissions.py

from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Permiso personalizado para permitir acceso solo a usuarios administradores.
    """
    def has_permission(self, request, view):
        # El usuario debe estar autenticado y tener el flag 'is_admin' en True.
        # El 'bool()' asegura que el resultado sea siempre True o False.
        return bool(request.user and request.user.is_authenticated and request.user.is_admin)