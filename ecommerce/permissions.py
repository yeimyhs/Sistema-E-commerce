from rest_framework.permissions import BasePermission, SAFE_METHODS

class AllowAnyForReadOnly(BasePermission):
    """
    Permite acceso sin autenticación solo a métodos seguros (GET, HEAD, OPTIONS).
    Para los demás métodos (POST, PUT, DELETE) se requiere autenticación.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:  # Métodos GET, HEAD, OPTIONS
            return True
        return request.user and request.user.is_authenticated  # Requiere autenticación para los demás métodos


class AllowRetrieveWithoutAuth(BasePermission):
    """
    Permite acceso sin autenticación solo a `retrieve` (GET con un ID específico).
    Los demás métodos requieren autenticación.
    """
    def has_permission(self, request, view):
        # Permitir solo autenticados por defecto
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Si es un GET con un objeto específico, permitir sin autenticación
        if request.method == "GET":
            return True
        return request.user and request.user.is_authenticated


from rest_framework.permissions import BasePermission, SAFE_METHODS

class AllowPostWithoutAuth(BasePermission):
    """
    Permite acceso sin autenticación solo a `POST`.  
    Los demás métodos requieren autenticación.
    """
    def has_permission(self, request, view):
        # Si es un POST, permitir sin autenticación
        if request.method == "POST":
            return True
        # Para otros métodos, requerir autenticación
        return request.user and request.user.is_authenticated
