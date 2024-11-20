import django_filters
from .models import Tblitem, Tblitemclasepropiedad, Tblitemclase, Tblitempropiedad

import django_filters

class TblitemclasepropiedadFilter(django_filters.FilterSet):
    clase_nombre = django_filters.CharFilter(field_name='idclase__nombre', lookup_expr='icontains')
    propiedad_nombre = django_filters.CharFilter(field_name='idpropiedad__nombre', lookup_expr='icontains')

    class Meta:
        model = Tblitemclasepropiedad
        fields = ['clase_nombre', 'propiedad_nombre']

from django_filters import rest_framework as filters


class TblitemFilter(filters.FilterSet):
    clase_nombre = filters.CharFilter(field_name='clases_propiedades__idclase__nombre', lookup_expr='icontains')
    propiedad_nombre = filters.CharFilter(field_name='clases_propiedades__idpropiedad__nombre', lookup_expr='icontains')

    class Meta:
        model = Tblitem
        fields = {
            'codigosku': ['icontains'],  # Filtro por SKU
            'descripcion': ['icontains'],  # Filtro por descripción
            'estado': ['exact'],  # Filtro por estado
            'idmarca': ['exact'],  # Filtro por marca
        }