import django_filters
from .models import Tblitem, tblitemclasevinculo, Tblitemclase, Tblitempropiedad, Tblpedido

import django_filters


from rest_framework import filters
from django.db.models import Q
from django.db import models

class TblitemclasepropiedadFilter(django_filters.FilterSet):
    clase_nombre = django_filters.CharFilter(field_name='idclase__nombre', lookup_expr='icontains')
    
    class Meta:
        model = tblitemclasevinculo
        fields = ['clase_nombre', 'propiedad']

from django_filters import rest_framework as filters

class TblitemFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name='fechacreacion', lookup_expr='gte')  # Filtro por fecha de creación desde
    end_date = filters.DateFilter(field_name='fechacreacion', lookup_expr='lte')  # Filtro por fecha de creación hasta
    

    clase_nombre = filters.CharFilter(field_name='clases_propiedades__idclase__nombre', lookup_expr='icontains')
    propiedad_nombre = filters.CharFilter(field_name='clases_propiedades__propiedad', lookup_expr='icontains')
    titulo = filters.CharFilter(field_name='titulo', lookup_expr='icontains')  # Filtro por título
    stock_min = filters.NumberFilter(field_name='stock', lookup_expr='gte')  # Filtro por stock mínimo
    stock_max = filters.NumberFilter(field_name='stock', lookup_expr='lte')  # Filtro por stock máximo
    destacado = filters.BooleanFilter(field_name='destacado')  # Filtro por destacado
    agotado = filters.BooleanFilter(field_name='agotado')  # Filtro por agotado
    nuevoproducto = filters.BooleanFilter(field_name='nuevoproducto')  # Filtro por nuevo producto
    preciorebajado_min = filters.NumberFilter(field_name='preciorebajado', lookup_expr='gte')  # Precio rebajado mínimo
    preciorebajado_max = filters.NumberFilter(field_name='preciorebajado', lookup_expr='lte')  # Precio rebajado máximo
    precionormal_min = filters.NumberFilter(field_name='precionormal', lookup_expr='gte')  # Precio normal mínimo
    precionormal_max = filters.NumberFilter(field_name='precionormal', lookup_expr='lte')  # Precio normal máximo
    fechacreacion_after = filters.DateFilter(field_name='fechacreacion', lookup_expr='gte')  # Fecha publicación después
    fechacreacion_before = filters.DateFilter(field_name='fechacreacion', lookup_expr='lte')  # Fecha publicación antes
    fechapublicacion_before = filters.DateFilter(field_name='fechapublicacion', lookup_expr='lte')  # Fecha publicación antes
    fechapublicacion_after = filters.DateFilter(field_name='fechapublicacion', lookup_expr='gte')  # Fecha publicación después
    peso_min = filters.NumberFilter(field_name='peso', lookup_expr='gte')  # Peso mínimo
    peso_max = filters.NumberFilter(field_name='peso', lookup_expr='lte')  # Peso máximo
    altura_min = filters.NumberFilter(field_name='altura', lookup_expr='gte')  # Altura mínima
    altura_max = filters.NumberFilter(field_name='altura', lookup_expr='lte')  # Altura máxima
    ancho_min = filters.NumberFilter(field_name='ancho', lookup_expr='gte')  # Ancho mínimo
    ancho_max = filters.NumberFilter(field_name='ancho', lookup_expr='lte')  # Ancho máximo
    profundidad_min = filters.NumberFilter(field_name='profundidad', lookup_expr='gte')  # Profundidad mínima
    profundidad_max = filters.NumberFilter(field_name='profundidad', lookup_expr='lte')  # Profundidad máxima

    class Meta:
        model = Tblitem
        fields = {
            'codigosku': ['icontains'],  # Filtro por SKU
            'descripcion': ['icontains'],  # Filtro por descripción
            'estado': ['exact'],  # Filtro por estado
            'idmodelo': ['exact'],  # Filtro por modelo
        }
        
from rest_framework.filters import BaseFilterBackend 
from django.utils import timezone

from django.utils.dateparse import parse_datetime
from django.utils import timezone
from datetime import datetime
import pytz
from django.utils.timezone import make_aware
from datetime import timezone
utc = timezone.utc
def parse_and_adjust_date(date_string, is_start_date=True):
    """
    Ajusta una fecha dada según sea la fecha inicial o final y la convierte a UTC usando Django.
    """
    date_format = "%Y-%m-%d"  # Formato de fecha esperado

    try:
        date_obj = datetime.strptime(date_string, date_format)
    except ValueError:
        raise ValueError(f"La fecha {date_string} no tiene el formato correcto {date_format}.")

    # Ajustar para la fecha inicial o final del día
    if is_start_date:
        date_obj = date_obj.replace(hour=0, minute=0, second=0)
    else:
        date_obj = date_obj.replace(hour=23, minute=59, second=59)

    # Asegurarnos de que la fecha sea timezone-aware
    return make_aware(date_obj, timezone.utc)

class DateTimeIntervalFilter(BaseFilterBackend):
    """
    Filtro personalizado para filtrar por intervalos de tiempo en campos DateTimeField.
    """
    def filter_queryset(self, request, queryset, view):
        # Obtener los parámetros de la URL
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        field_name = request.GET.get('field_name', 'fechacreacion')  # Campo predeterminado

        # Validar los parámetros necesarios
        if not hasattr(queryset.model, field_name):
            print(f"El campo {field_name} no existe en el modelo {queryset.model.__name__}.")
            return queryset

        # Ajustar las fechas si están disponibles
        start_date = parse_and_adjust_date(start_date, is_start_date=True) if start_date else None
        end_date = parse_and_adjust_date(end_date, is_start_date=False) if end_date else None

        print(f"Fechas ajustadas: start_date={start_date}, end_date={end_date}")

        # Verificar si el campo especificado es de tipo DateTimeField
        field = queryset.model._meta.get_field(field_name)
        if not isinstance(field, models.DateTimeField):
            print(f"El campo {field_name} no es un DateTimeField. Filtro no aplicado.")
            return queryset

        # Filtrar el queryset según las fechas
        if start_date and end_date:
            return queryset.filter(
                Q(**{f'{field_name}__gte': start_date}) & Q(**{f'{field_name}__lte': end_date})
            )
        elif start_date:
            return queryset.filter(Q(**{f'{field_name}__gte': start_date}))
        elif end_date:
            return queryset.filter(Q(**{f'{field_name}__lte': end_date}))

        print("No se aplicó ningún filtro porque no se especificaron fechas.")
        return queryset
    
    

class TblpedidoFilter(filters.FilterSet):
    sin_transaccion = filters.BooleanFilter(method='filter_sin_transaccion')

    class Meta:
        model = Tblpedido
        fields = ['activo', 'idpedido', 'idcliente_id', 'subtotal', 'total', 'igv', 'totaldescuento', 'idcupon_id', 'idmoneda_id', 'idtransaccion_id', 'estado', 'fechacreacion', 'fechamodificacion']

    def filter_sin_transaccion(self, queryset, name, value):
        if value:
            return queryset.filter(idtransaccion__isnull=True)
        elif value == False:
            return queryset.filter(idtransaccion__isnull=False)
        return queryset