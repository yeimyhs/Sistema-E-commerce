from rest_framework.viewsets import ModelViewSet
from ecommerce.serializers import AdministracionSerializer, CuponSerializer, MarcaSerializer, MonedaSerializer, PromocionSerializer, TblcarritoSerializer, TblitemSerializer, TblnoticiaSerializer, TblpedidoSerializer, TblCarruselSerializer, TipocambioSerializer, ValoracionSerializer, TbldetallecarritoSerializer, TblimagenitemSerializer, TblitemclaseSerializer, TblitempropiedadSerializer, TblitemrelacionadoSerializer, TbldetallepedidoSerializer
from ecommerce.models import Administracion, Cupon, Marca, Moneda, Promocion, Tblcarrito, Tblitem, Tblnoticia, Tblpedido, TblCarrusel, Tipocambio, Valoracion, Tbldetallecarrito, Tblimagenitem, Tblitemclase, Tblitempropiedad, Tblitemrelacionado, Tbldetallepedido

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
#from .filters import TblitemFilter

from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


import requests
from requests.auth import HTTPBasicAuth
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt

def create_payment(request):
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)  # Asegúrate de convertir el cuerpo a JSON
            url = "https://api.micuentaweb.pe/api-payment/V4/Charge/CreatePayment"
            
            # Imprimir el payload para verificar que estás enviando los datos correctamente
            print("Payload:", payload)

            response = requests.post(
                url,
                auth=HTTPBasicAuth(settings.IZIPAY_USERNAME, settings.IZIPAY_PASSWORD),
                json=payload
            )
            
            # Imprimir la respuesta para ver qué devuelve el servidor
            print("Response Status Code:", response.status_code)
            print("Response Body:", response.text)

            if response.status_code == 200:
                return JsonResponse(response.json(), status=200)
            else:
                # Si hay error, devolver el mensaje y el código de estado
                return JsonResponse({
                    "status": "error", 
                    "message": response.json()
                }, status=400)
        
        except Exception as e:
            # Capturar el error completo y devolverlo en la respuesta
            print(f"Error: {e}")
            return JsonResponse({"status": "error", "message": "Hubo un error al procesar la solicitud."}, status=500)
    
    else:
        return JsonResponse({"status": "error", "message": "Método no permitido."}, status=405)
    
class ClasesYPropiedadesView(APIView):
    def get(self, request):
        # Inicializa una lista para almacenar las clases y sus propiedades
        clases_propiedades = []
        
        # Obtiene todas las clases y sus propiedades relacionadas
        clases = Tblitemclase.objects.all().prefetch_related('tblitempropiedad_set')
        
        # Agrupa las propiedades por clase
        for clase in clases:
            vinculos = tblitemclasevinculo.objects.filter(idclase=clase, activo=True).values('propiedad').distinct()

# Construir la lista de propiedades únicas
            propiedades_list = [{ "nombre": v['propiedad']} for v in vinculos]

            clases_propiedades.append({
                "idclase": clase.idclase,
                "clase": clase.nombre,
                "propiedades": propiedades_list
            })

        # Retorna la respuesta
        return Response(clases_propiedades)
    
class BusquedaDinamicaViewSet(viewsets.ViewSet):
    serializer_class = TblitemSerializer
    @swagger_auto_schema(
        operation_description="Busca productos filtrados por combinaciones de clase y propiedad. " 
                              "Se pueden agregar múltiples combinaciones separadas por '&'.",
        manual_parameters=[
            openapi.Parameter(
                name='clase',
                in_=openapi.IN_QUERY,
                description="Combinaciones de clase y propiedad para filtrar los productos. "
                            "Ejemplo: ?clase=1,propiedad=1&clase=1,propiedad=2",
                type=openapi.TYPE_STRING,
                required=True,
                examples={
                    "query": "1,propiedad=1"
                }
            ),
        ],
        responses={200: TblitemSerializer(many=True)},
    )
    
    def list(self, request):
        query = Q()  # Inicializamos una consulta vacía

        for filtro in request.query_params.getlist("clase"):
            # Dividimos el valor en clase y propiedad
            if "propiedad=" in filtro:
                try:
                    clase, propiedad = filtro.split(",propiedad=")
                    # Agregamos la combinación a la consulta con OR
                    query |= Q(
                        clases_propiedades__idclase=clase,
                        clases_propiedades__propiedad__iexact=propiedad.strip()  # Comparación case-insensitive
                    )
                except ValueError:
                    continue  # Si no tiene el formato esperado, lo ignoramos

        # Filtramos los items que cumplen con la consulta
        items = Tblitem.objects.filter(query).distinct()
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
        response = super(LoginView, self).post(request, format=None)
        
        # Serializar la información completa del usuario
        user_serializer = CustomUserSerializer(user)
        
        # Combinar el token con los datos serializados del usuario
        response.data["user"] = user_serializer.data
        
        return response

    def throttled(self, request, wait):
        return Response(
            {"error": "Too many failed login attempts, please try again later"},
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
    search_fields = ['nombreempresa', 'ruc', 'telefono', 'idmoneda__nombre']
    filterset_fields = ['activo', 'nombreempresa', 'ruc', 'telefono', 'igv', 'idmoneda_id', 'idmoneda__nombre', 'fechacreacion', 'fechamodificacion']



class CuponViewSet(ModelViewSet):
    queryset = Cupon.objects.order_by('pk')
    serializer_class = CuponSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['descripcion', 'estado', 'fechavigencia']
    filterset_fields = ['activo', 'idcupon', 'cantidaddescuento', 'estado', 'fechavigencia', 'fechacreacion', 'fechamodificacion']



class MarcaViewSet(ModelViewSet):
    queryset = Marca.objects.order_by('pk')
    serializer_class = MarcaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nombre']
    filterset_fields = ['activo', 'id', 'nombre']


class TblreclamacionViewSet(ModelViewSet):
    queryset = Tblreclamacion.objects.order_by('pk')
    serializer_class = TblreclaisionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nombre']
    filterset_fields = '__all__'



class MarcaViewSet(ModelViewSet):
    queryset = Marca.objects.order_by('pk')
    serializer_class = MarcaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nombre']
    filterset_fields = ['activo', 'id', 'nombre']

class TblcategoriaViewSet(ModelViewSet):
    queryset = Tblcategoria.objects.order_by('pk')
    serializer_class = TblcategoriaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nombre']
    filterset_fields = ['activo', 'id', 'nombre']

class TblmodeloViewSet(ModelViewSet):
    queryset = Tblmodelo.objects.order_by('pk')
    serializer_class = TblmodeloSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nombre']
    filterset_fields = ['activo', 'id', 'nombre', 'idmarca_id']




class MonedaViewSet(ModelViewSet):
    queryset = Moneda.objects.order_by('pk')
    serializer_class = MonedaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nombre']
    filterset_fields = ['activo', 'idmoneda', 'nombre', 'estado', 'fechacreacion', 'fechamodificacion']



class PromocionViewSet(ModelViewSet):
    queryset = Promocion.objects.order_by('pk')
    serializer_class = PromocionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = [ 'estado']
    filterset_fields = ['activo', 'idpromocion', 'estado', 'fechacreacion', 'fechamodificacion']


class TblcarritoViewSet(ModelViewSet):
    queryset = Tblcarrito.objects.order_by('pk')
    serializer_class = TblcarritoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['idusuario__nombreusuario', 'preciototal']
    filterset_fields = ['activo', 'idusuario_id', 'preciototal']

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from .models import Tblitem
from .serializers import TblitemSerializer
from .filters import TblitemclasepropiedadFilter
from .filters import *
from rest_framework import filters

class TblitemViewSet(ModelViewSet):
    queryset = Tblitem.objects.prefetch_related(
        'clases_propiedades',
        'clases_propiedades__idclase',
        'clases_propiedades__idpropiedad' # Prefetch para las propiedades
    ).all()
    serializer_class = TblitemSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend,DateTimeIntervalFilter]
    filterset_class = TblitemFilter
    
    # Agrega campos relacionados para la búsqueda
    search_fields = [
        'codigosku',  # Campo directo de Tblitem
        'descripcion',  # Campo directo de Tblitem
        'clases_propiedades__idclase__nombre',  # Nombre de la clase relacionada
        'clases_propiedades__idpropiedad__nombre'  # Nombre de la propiedad relacionada
    ]
    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        # Solo usuarios admin pueden ver los cupones completos
        if self.request.user.is_staff:
            return Tblitem.objects.prefetch_related('cupon_relacionado')  # Optimización
        # Si no es admin, excluir cupones relacionados
        return Tblitem.objects.all()



class TblnoticiaViewSet(ModelViewSet):
    queryset = Tblnoticia.objects.order_by('pk')
    serializer_class = TblnoticiaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['descripcion', 'estado']
    filterset_fields = ['activo', 'idnoticia', 'descripcion', 'estado', 'fechacreacion', 'fechamodificacion']


class TblsedeViewSet(ModelViewSet):
    queryset = Tblsede.objects.order_by('pk')
    serializer_class = TblsedeSerializer

class TblpedidoViewSet(ModelViewSet):
    queryset = Tblpedido.objects.order_by('pk')
    serializer_class = TblpedidoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['idcliente__nombreusuario', 'total', 'estado']
    filterset_fields = ['activo', 'idpedido', 'idcliente_id', 'subtotal', 'total', 'igv', 'totaldescuento', 'idcupon_id', 'idmoneda_id', 'estado', 'fechacreacion', 'fechamodificacion']



class TblCarruselViewSet(ModelViewSet):
    queryset = TblCarrusel.objects.order_by('pk')
    serializer_class = TblCarruselSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['descripcion', 'estado']
    filterset_fields = ['activo', 'id',  'descripcion', 'estado', 'fechacreacion', 'fechamodificacion']



class TblusuarioViewSet(ModelViewSet):
    queryset = CustomUser.objects.order_by('pk')
    serializer_class = CustomUserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nombreusuario', 'nombre', 'apellidos', 'estado']
    filterset_fields = ['activo', 'nombreusuario', 'nombre', 'apellidos','departamento','provincia','distrito','telefono', 'estado', 'email_verified_at', 'direccion', 'fechacreacion', 'fechamodificacion','is_staff']



class TipocambioViewSet(ModelViewSet):
    queryset = Tipocambio.objects.order_by('pk')
    serializer_class = TipocambioSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['tipocambio', 'idmoneda__nombre', 'fechacreacion', 'fechamodificacion']
    filterset_fields = ['activo', 'tipocambio', 'idmoneda__nombre', 'fechacreacion', 'fechamodificacion']




class ValoracionViewSet(ModelViewSet):
    queryset = Valoracion.objects.order_by('pk')
    serializer_class = ValoracionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['comentario', 'estrellas']
    filterset_fields = ['activo', 'idvaloracion', 'estrellas', 'comentario', 'estado', 'telefono', 'idproduct_id', 'fechacreacion', 'fechamodificacion']

    


class TbldetallecarritoViewSet(ModelViewSet):
    queryset = Tbldetallecarrito.objects.order_by('pk')
    serializer_class = TbldetallecarritoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['idproduct__descripcion', 'cantidad']
    filterset_fields = ['activo',  'idproduct_id', 'cantidad', 'isuser_id', 'idcupon_id']



class TblimagenitemViewSet(ModelViewSet):
    queryset = Tblimagenitem.objects.order_by('pk')
    serializer_class = TblimagenitemSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['imagen', 'idproduct__descripcion']
    filterset_fields = ['activo', 'idimagen', 'idproduct_id', 'estado']
    
    @action(detail=False, methods=['post'], url_path='upload-multiple')
    def upload_multiple(self, request):
        """
        Endpoint personalizado para subir múltiples imágenes relacionadas a un producto.
        """
        serializer = MultipleImagenItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Imágenes subidas exitosamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class MultipleImagenItemView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MultipleImagenItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Imágenes subidas exitosamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class TblitemclaseViewSet(ModelViewSet):
    queryset = Tblitemclase.objects.order_by('pk')
    serializer_class = TblitemclaseSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nombre']
    filterset_fields = ['activo', 'idclase', 'nombre']

class tblitemcuponSerializerViewSet(ModelViewSet):
    queryset = tblitemcupon.objects.order_by('pk')
    serializer_class = tblitemcuponSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nombre']
    filterset_fields = ['activo', 'id', 'iditem_id', 'idcupon_id']



class tblitemclasevinculoViewSet(ModelViewSet):
    queryset = tblitemclasevinculo.objects.order_by('pk')
    serializer_class = TblitemclasevinculoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = [ 'propiedad', 'idclase__nombre']
    filterset_fields = ['activo', 'id', 'iditem_id', 'propiedad', 'idclase_id']



class TblitempropiedadViewSet(ModelViewSet):
    queryset = Tblitempropiedad.objects.order_by('pk')
    serializer_class = TblitempropiedadSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nombre', 'idclase__nombre']
    filterset_fields = ['activo', 'idpropiedad', 'nombre', 'idclase_id']
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
    search_fields = ['item_id__descripcion']
    filterset_fields = ['activo', 'item_id', 'item_relacionado_id']


class tblitemcategoriaViewSet(ModelViewSet):
    queryset = tblitemcategoria.objects.order_by('pk')
    serializer_class = tblitemcategoriaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['iditem_id__descripcion']
    filterset_fields = ['activo', 'iditem_id']




class TbldetallepedidoViewSet(ModelViewSet):
    queryset = Tbldetallepedido.objects.order_by('pk')
    serializer_class = TbldetallepedidoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['idpedido__id', 'idproduct__descripcion']
    filterset_fields = ['activo', 'idpedido_id', 'idproduct_id', 'cantidad', 'preciototal', 'preciunitario']
