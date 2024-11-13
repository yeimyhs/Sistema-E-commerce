import django_filters
from .models import Tblitem, Tblitemclasepropiedad, Tblitemclase, Tblitempropiedad

class TblitemFilter(django_filters.FilterSet):
    # Filtro por nombre de clase a través de Tblitemclasepropiedad
    clase_nombre = django_filters.CharFilter(
        field_name='tblitemclasepropiedad__idclase__nombre', lookup_expr='icontains'
    )
    
    # Filtro por nombre de propiedad a través de Tblitemclasepropiedad
    propiedad_nombre = django_filters.CharFilter(
        field_name='tblitemclasepropiedad__idpropiedad__nombre', lookup_expr='icontains'
    )

    class Meta:
        model = Tblitem
        fields = []  # No estamos filtrando por campos directamente en Tblitem
