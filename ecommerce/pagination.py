from rest_framework.pagination import LimitOffsetPagination

class NoMaxLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10  # Si el cliente no especifica "limit", se usa 10
    max_limit = None  # Permite cualquier número si "limit" se especifica en la URL
