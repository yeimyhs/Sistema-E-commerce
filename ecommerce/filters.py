import django_filters
from .models import Tblitem, Tblitemclasepropiedad, Tblitemclase, Tblitempropiedad

import django_filters


from rest_framework import filters
from django.db.models import Q
from django.db import models

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
            #'idmarca': ['exact'],  # Filtro por marca
        }
        
from rest_framework.filters import BaseFilterBackend 
from django.utils import timezone

from django.utils.dateparse import parse_datetime
from django.utils import timezone
from datetime import datetime

def format_date(date_string):
    # Intentar parsear la fecha
    try:
        # Parsear la fecha de entrada
        date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")
        # Añadir los microsegundos (rellenar con ceros)
        date = date.replace(microsecond=0)
        # Asegurar la zona horaria (puedes hacer que sea aware si es necesario)
        return timezone.make_aware(date)
    except ValueError:
        return None
    
class DateTimeIntervalFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # Obtener los parámetros de la URL
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        field_name = request.GET.get('field_name')  # El nombre del campo a filtrar
        print("===================se esta usando el filtrooooS")
        print(start_date)
        print(end_date)
        start_date = format_date(request.GET.get('start_date'))
        end_date = format_date(request.GET.get('end_date'))
        print(start_date)
        print(end_date)
        # Verificar si 'start_date' y 'end_date' son proporcionados
        if start_date or end_date:
            # Validar que el 'field_name' corresponde a un campo DateTimeField del modelo
            if field_name and hasattr(queryset.model, field_name):
                field = getattr(queryset.model, field_name)

                # Si el campo es un DateTimeField, aplicamos el filtro
                if isinstance(field, models.DateTimeField):
                    if start_date and end_date:
                        queryset = queryset.filter(
                            Q(**{f'{field_name}__gte': start_date}) & 
                            Q(**{f'{field_name}__lte': end_date})
                        )
                        print("===============",queryset)

                    elif start_date:
                        queryset = queryset.filter(**{f'{field_name}__gte': start_date})
                    elif end_date:
                        queryset = queryset.filter(**{f'{field_name}__lte': end_date})
        print(queryset)
        return queryset