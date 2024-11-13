from rest_framework.viewsets import ModelViewSet
from ecommerce.serializers import AdministracionSerializer, CuponSerializer, MarcaSerializer, MonedaSerializer, PromocionSerializer, TblcarritoSerializer, TblitemSerializer, TblnoticiaSerializer, TblpedidoSerializer, TblsliderSerializer, TipocambioSerializer, ValoracionSerializer, TbldetallecarritoSerializer, TblimagenitemSerializer, TblitemclaseSerializer, TblitemclasepropiedadSerializer, TblitempropiedadSerializer, TblitemrelacionadoSerializer, TbldetallepedidoSerializer
from ecommerce.models import Administracion, Cupon, Marca, Moneda, Promocion, Tblcarrito, Tblitem, Tblnoticia, Tblpedido, Tblslider, Tipocambio, Valoracion, Tbldetallecarrito, Tblimagenitem, Tblitemclase, Tblitemclasepropiedad, Tblitempropiedad, Tblitemrelacionado, Tbldetallepedido

from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics

from rest_framework import filters

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from knox.models import AuthToken

from .models import *
from .serializers import *

from rest_framework.decorators import action
from rest_framework import filters
from .filters import TblitemFilter

from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response

class ClasesYPropiedadesView(APIView):
    def get(self, request):
        # Inicializa una lista para almacenar las clases y sus propiedades
        clases_propiedades = []
        
        # Obtiene todas las clases y sus propiedades relacionadas
        clases = Tblitemclase.objects.all().prefetch_related('tblitempropiedad_set')
        
        # Agrupa las propiedades por clase
        for clase in clases:
            propiedades = Tblitempropiedad.objects.filter(idclase=clase)
            propiedades_list = [{"idpropiedad": p.idpropiedad, "nombre": p.nombre} for p in propiedades]
            clases_propiedades.append({
                "idclase": clase.idclase,
                "clase": clase.nombre,
                "propiedades": propiedades_list
            })

        # Retorna la respuesta
        return Response(clases_propiedades)
    
class BusquedaDinamicaViewSet(viewsets.ViewSet):
    def list(self, request):
        # Construimos la consulta Q de manera dinámica según las clases y propiedades en los parámetros de la URL
        query = Q()
        
        # Iterar sobre todos los parámetros de la solicitud
        for key, value in request.query_params.items():
            # Esperamos que el nombre del parámetro esté en el formato clase_propiedad
            if "_" in key:
                clase, propiedad = key.split("_", 1)
                query &= Q(
                    clases_propiedades__idclase__nombre=clase,
                    clases_propiedades__idpropiedad__nombre=value
                )

        # Filtra los productos basados en la consulta generada
        items = Tblitem.objects.filter(query).distinct()

        # Serializa y retorna la respuesta
        serializer = TblitemSerializer(items, many=True)
        return Response(serializer.data)


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = CustomAuthTokenSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return Response({"error": "El nombreusuario y el password son obligatorios"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.validated_data.get('nombreusuario')
        if user is None:
            return Response({"error": "Credenciales Invalidas"}, status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser.objects.filter(nombreusuario=user).first()
        if not user.estado:
            return Response({"error": "Cuenta deshabilitada"}, status=status.HTTP_403_FORBIDDEN)
        
        login(request, user)
        return super(LoginView, self).post(request, format=None)

    def throttled(self, request, wait):
        return Response(
            {"error": "Too many failed login attempts, please try again later"},
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": serializer.data,
            
            "token": AuthToken.objects.create(user)[1]
        })



class AdministracionViewSet(ModelViewSet):
    queryset = Administracion.objects.order_by('pk')
    serializer_class = AdministracionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nombreempresa', 'ruc', 'telefono', 'moneda__nombre']
    filterset_fields = ['nombreempresa', 'ruc', 'telefono', 'igv', 'moneda_id', 'moneda__nombre', 'fechacreacion', 'fechamodificacion']



class CuponViewSet(ModelViewSet):
    queryset = Cupon.objects.order_by('pk')
    serializer_class = CuponSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['descripcion', 'estado', 'fechavigencia']
    filterset_fields = ['idcupon', 'cantidaddescuento', 'estado', 'fechavigencia', 'fechacreacion', 'fechamodificacion']



class MarcaViewSet(ModelViewSet):
    queryset = Marca.objects.order_by('pk')
    serializer_class = MarcaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nombre']
    filterset_fields = ['id', 'nombre', 'imgen']



class MonedaViewSet(ModelViewSet):
    queryset = Moneda.objects.order_by('pk')
    serializer_class = MonedaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nombre']
    filterset_fields = ['idmoneda', 'nombre', 'estado', 'fechacreacion', 'fechamodificacion']



class PromocionViewSet(ModelViewSet):
    queryset = Promocion.objects.order_by('pk')
    serializer_class = PromocionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['imagenpromocion', 'estado']
    filterset_fields = ['idpromocion', 'imagenpromocion', 'estado', 'fechacreacion', 'fechamodificacion']


class TblcarritoViewSet(ModelViewSet):
    queryset = Tblcarrito.objects.order_by('pk')
    serializer_class = TblcarritoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['idusuario__nombreusuario', 'preciototal']
    filterset_fields = ['idusuario_id', 'preciototal']



class TblitemViewSet(ModelViewSet):
    queryset = Tblitem.objects.prefetch_related(
        'tblitemclasepropiedad_set',  # Prefetch Tblitemclasepropiedad para evitar múltiples consultas
        'tblitemclasepropiedad_set__idclase',  # Prefetch las clases
        'tblitemclasepropiedad_set__idpropiedad'  # Prefetch las propiedades
    ).all()
    serializer_class = TblitemSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = TblitemFilter



class TblnoticiaViewSet(ModelViewSet):
    queryset = Tblnoticia.objects.order_by('pk')
    serializer_class = TblnoticiaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['descripcion', 'estado']
    filterset_fields = ['idnoticia', 'imagennoticia', 'descripcion', 'estado', 'fechacreacion', 'fechamodificacion']



class TblpedidoViewSet(ModelViewSet):
    queryset = Tblpedido.objects.order_by('pk')
    serializer_class = TblpedidoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['idcliente__nombreusuario', 'total', 'estado']
    filterset_fields = ['idpedido', 'idcliente_id', 'subtotal', 'total', 'igv', 'totaldescuento', 'idcupon_id', 'idmoneda_id', 'estado', 'fechacreacion', 'fechamodificacion']



class TblsliderViewSet(ModelViewSet):
    queryset = Tblslider.objects.order_by('pk')
    serializer_class = TblsliderSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['descripcion', 'estado']
    filterset_fields = ['id', 'imagen', 'descripcion', 'estado', 'fechacreacion', 'fechamodificacion']



class TblusuarioViewSet(ModelViewSet):
    queryset = CustomUser.objects.order_by('pk')
    serializer_class = CustomUserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nombreusuario', 'nombre', 'apellidos', 'estado']
    filterset_fields = ['nombreusuario', 'nombre', 'apellidos', 'estado', 'email_verified_at', 'direccion', 'fechacreacion', 'fechamodificacion']



class TipocambioViewSet(ModelViewSet):
    queryset = Tipocambio.objects.order_by('pk')
    serializer_class = TipocambioSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['tipocambio', 'idmoneda__nombre', 'fechacreacion', 'fechamodificacion']
    filterset_fields = ['tipocambio', 'idmoneda__nombre', 'fechacreacion', 'fechamodificacion']




class ValoracionViewSet(ModelViewSet):
    queryset = Valoracion.objects.order_by('pk')
    serializer_class = ValoracionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['comentario', 'estrellas']
    filterset_fields = ['idvaloracion', 'estrellas', 'comentario', 'estado', 'telefono', 'idproduct_id', 'idmoneda_id', 'fechacreacion', 'fechamodificacion']

    


class TbldetallecarritoViewSet(ModelViewSet):
    queryset = Tbldetallecarrito.objects.order_by('pk')
    serializer_class = TbldetallecarritoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['idproduct__descripcion', 'cantidad']
    filterset_fields = ['idpedido_id', 'idproduct_id', 'cantidad', 'preciototal', 'preciunitario']



class TblimagenitemViewSet(ModelViewSet):
    queryset = Tblimagenitem.objects.order_by('pk')
    serializer_class = TblimagenitemSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['imagen', 'idproduct__descripcion']
    filterset_fields = ['idimagen', 'idproduct_id', 'imagen', 'estado']



class TblitemclaseViewSet(ModelViewSet):
    queryset = Tblitemclase.objects.order_by('pk')
    serializer_class = TblitemclaseSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nombre']
    filterset_fields = ['idclase', 'nombre']



class TblitemclasepropiedadViewSet(ModelViewSet):
    queryset = Tblitemclasepropiedad.objects.order_by('pk')
    serializer_class = TblitemclasepropiedadSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['idproduct__descripcion', 'idpropiedad__nombre', 'idclase__nombre']
    filterset_fields = ['id', 'idproduct_id', 'idpropiedad_id', 'idclase_id']



class TblitempropiedadViewSet(ModelViewSet):
    queryset = Tblitempropiedad.objects.order_by('pk')
    serializer_class = TblitempropiedadSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nombre', 'idclase__nombre']
    filterset_fields = ['idpropiedad', 'nombre', 'idclase_id']
    @action(detail=False, methods=['get'], url_path='por-clase/(?P<clase_id>\d+)')
    def por_clase(self, request, clase_id=None):
        """
        Retorna todas las itempropiedades relacionadas a una clase de item específica.
        """
        propiedades = Tblitempropiedad.objects.filter(idclase=clase_id)
        serializer = TblitempropiedadSerializer(propiedades, many=True)
        return Response(serializer.data)




class TblitemrelacionadoViewSet(ModelViewSet):
    queryset = Tblitemrelacionado.objects.order_by('pk')
    serializer_class = TblitemrelacionadoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['idproduct__descripcion']
    filterset_fields = ['idproduct_id', 'fk_id']



class TbldetallepedidoViewSet(ModelViewSet):
    queryset = Tbldetallepedido.objects.order_by('pk')
    serializer_class = TbldetallepedidoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['idpedido__id', 'idproduct__descripcion']
    filterset_fields = ['idpedido_id', 'idproduct_id', 'cantidad', 'preciototal', 'preciunitario']
