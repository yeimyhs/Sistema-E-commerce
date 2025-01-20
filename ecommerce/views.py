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
from .filters import *

from rest_framework.decorators import action
from rest_framework import filters
#from .filters import TblitemFilter

from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


import rarfile
import os
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from .models import Tblitem
import os
import rarfile
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Tblitem
from django.conf import settings


from rest_framework.generics import ListAPIView

rarfile.UNRAR_TOOL = r"C:\Program Files\WinRAR\UnRAR.exe"
@csrf_exempt
def upload_images(request):
    """
    Servicio POST para subir un archivo RAR que contiene imágenes y asociarlas con los productos usando el SKU.
    """
    # Verificar que el archivo RAR esté presente en la solicitud
    if 'rar_file' not in request.FILES:
        return JsonResponse({'error': 'No se proporcionó un archivo RAR'}, status=400)

    rar_file = request.FILES['rar_file']

    # Guardar temporalmente el archivo RAR en el sistema
    rar_file_path = os.path.join(settings.MEDIA_ROOT, 'temp.rar')
    with open(rar_file_path, 'wb') as f:
        for chunk in rar_file.chunks():
            f.write(chunk)

    try:
        # Abrir el archivo RAR y procesar las imágenes
        with rarfile.RarFile(rar_file_path) as rf:
            # Iterar sobre los archivos dentro del RAR
            for archivo in rf.infolist():
                if archivo.is_file() and archivo.filename.lower().endswith('.jpg'):
                    # Obtener el SKU del nombre de la imagen
                    nombre_imagen = archivo.filename
                    sku_imagen = nombre_imagen.split('/')[-1].split('.')[0]  # Eliminar cualquier prefijo y la barra
 # El SKU es todo antes de .jpg
                    print(sku_imagen)
                    # Buscar el producto en la base de datos por el SKU
                    try:
                        producto = Tblitem.objects.get(codigosku=sku_imagen)
                    except Tblitem.DoesNotExist:
                        print(f"No se encontró el producto con SKU {sku_imagen}")
                        continue

                    # Extraer la imagen
                    with rf.open(archivo) as f:
                        imagen_bytes = f.read()
                        imagen = Image.open(BytesIO(imagen_bytes))

                        # Guardar la imagen en el campo imagenprincipal del producto
                        imagen.name = archivo.filename  # Asignar el nombre original de la imagen
                        imagen_path = os.path.join(settings.MEDIA_ROOT, 'imagenPrincipalItem', nombre_imagen)

                        # Guardar la imagen en el sistema de archivos
                        imagen.save(imagen_path)

                        # Asignar la imagen al campo 'imagenprincipal' del producto
                        with open(imagen_path, 'rb') as image_file:
                            producto.imagenprincipal = File(image_file, nombre_imagen)
                            producto.save()

                    print(f"Imagen para SKU {sku_imagen} guardada exitosamente.")
        
        # Eliminar el archivo temporal
        os.remove(rar_file_path)

        return JsonResponse({'message': 'Imágenes procesadas y asociadas correctamente'}, status=200)

    except Exception as e:
        # Manejo de errores si ocurre algún problema
        return JsonResponse({'error': str(e)}, status=500)

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
    
    
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from requests.auth import HTTPBasicAuth
import json

# URL del servicio externo

# Credenciales

@csrf_exempt
def generate_token(request):
    """
    Vista para generar un token a través del servicio CreateToken.
    "currency": "PEN",  # Ejemplo de moneda
    "customer": {
        "email":"ejemplo@otro.com"
    }
    """
    if request.method == "POST":
        try:
            # Parsear el cuerpo de la solicitud
            payload = json.loads(request.body)
            TOKEN_URL = "https://api.micuentaweb.pe/api-payment/V4/Charge/CreateToken"
            
            # Enviar solicitud POST al servicio externo
            response = requests.post(
                TOKEN_URL,
                auth=HTTPBasicAuth(settings.IZIPAY_USERNAME, settings.IZIPAY_PASSWORD),
                #auth=HTTPBasicAuth(USERNAME, PASSWORD),
                json=payload
            )
            
            # Verificar el estado de la respuesta
            if response.status_code == 200:
                return JsonResponse(response.json(), status=200)
            else:
                return JsonResponse({
                    "error": "Error al generar el token",
                    "status_code": response.status_code,
                    "details": response.text
                }, status=response.status_code)
        
        except Exception as e:
            # Manejar errores y retornar una respuesta apropiada
            return JsonResponse({"error": str(e)}, status=500)
    
    # Método no permitido
    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def create_token(request):
    """
    Vista para la creación de un token de tarjeta.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            url = f"{BASE_API_URL}tokens"
            response = requests.post(url, headers=HEADERS, json=data)
            return JsonResponse(response.json(), status=response.status_code)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def get_token(request):
    """
    Vista para consultar datos de un token específico.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            url = f"{BASE_API_URL}tokens/token"
            response = requests.post(url, headers=HEADERS, json=data)
            return JsonResponse(response.json(), status=response.status_code)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def get_tokens_by_buyer(request):
    """
    Vista para consultar todos los tokens registrados para un comprador.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            url = f"{BASE_API_URL}tokens/tokens"
            response = requests.post(url, headers=HEADERS, json=data)
            return JsonResponse(response.json(), status=response.status_code)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Método no permitido"}, status=405)




import hmac
import hashlib
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import hashlib

from cryptography.hazmat.primitives import hmac, hashes
from cryptography.hazmat.backends import default_backend


# Define tu clave secreta
SHA_KEY = "TSEyml51VjdNpO9lA9BILIRUF8Ew6cLI2exAw2LstUBN9"  # Reemplaza con tu clave HMAC-SHA-256
def check_hash(data, key):
    """
    Verifica la firma del mensaje usando HMAC-SHA256
    """
    supported_sign_algos = ['sha256_hmac']
    alg = data.get('kr-hash-algorithm')

    # Validar el algoritmo de hash
    if alg not in supported_sign_algos:
        return False

    # Obtener el contenido de 'kr-answer' y asegurarse de que sea una cadena JSON
    kr_answer = json.dumps(data.get('kr-answer', {}), separators=(',', ':'))
    kr_answer = kr_answer.replace('\\/', '/')

    # Calcular el hash HMAC-SHA256
    calculated_hash = hmac.HMAC(key.encode('utf-8'),
                hashes.SHA256(),
                backend=default_backend())
    calculated_hash.update(kr_answer.encode('utf-8'))
    calculated_hash = calculated_hash.finalize().hex()

    # Comparar con el hash recibido
    received_hash = data.get('kr-hash')
    return calculated_hash == received_hash

from django.utils.timezone import now
from decimal import Decimal
from django.db import transaction

@csrf_exempt
@transaction.atomic
def process_payment(request):
    if request.method != 'POST':
        return HttpResponse('Método no permitido', status=405)
    
    try:
        # Decodificar el JSON recibido
        data = json.loads(request.body.decode('utf-8'))
        # PASO 1: verificar la firma con SHA_KEY
        if not check_hash(data, SHA_KEY):
            return HttpResponse('Invalid signature.<br/>', status=400)
   
        
        # Preparar la respuesta siguiendo el formato original
        answer = {
            'message':'OK',
            'kr-hash': data.get('kr-hash'),
            'kr-hash-algorithm': data.get('kr-hash-algorithm'),
            'kr-answer-type': data.get('kr-answer-type'),
            'kr-answer': data.get('kr-answer')
        }
        transaccion_data = data.get("kr-answer", {}).get("transactions", [])[0]
        card_details = transaccion_data.get("transactionDetails", {}).get("cardDetails", {})
        authorization_response = card_details.get("authorizationResponse", {})
        user_info = transaccion_data.get("transactionDetails", {}).get("userInfo", "DESCONOCIDO")
        idpedido = data.get("kr-answer", {}).get("orderDetails", {}).get("orderId")
        # Crear nueva transacción
        nueva_transaccion = tblTransaccion.objects.create(
            transaccion_id=transaccion_data.get("uuid"),
            metodo_pago=transaccion_data.get("paymentMethodType", "DESCONOCIDO"),
            nombre_en_tarjeta=card_details.get("cardHolderName")or user_info,
            numero_tarjeta=card_details.get("pan", "XXXX XXXX XXXX XXXX"),
            monto_total=Decimal(authorization_response.get("amount", 0)) / 100,  # Asumimos que el monto está en centavos
            fecha_transaccion=authorization_response.get("authorizationDate", now())
        )
        
        pedido = Tblpedido.objects.get(idpedido=idpedido)
        pedido.idtransaccion = nueva_transaccion
        pedido.save()
        # Devolver la respuesta en formato JSON
        return HttpResponse(
            json.dumps(answer),
            content_type='application/json'
        )
        
    except json.JSONDecodeError:
        return HttpResponse('Invalid JSON', status=400)
    except Exception as e:
        return HttpResponse(str(e), status=500)
    
    
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count


class ClasesYPropiedadesView(APIView):
    def post(self, request):
        # JSON de entrada
        filtros = request.data

        # "filtro general"
        filtro_general = []
        clases = Tblitemclase.objects.all().prefetch_related('tblitempropiedad_set')
        
        for clase in clases:
            vinculos = tblitemclasevinculo.objects.filter(
                idclase=clase, activo=True
            ).values('propiedad').distinct()

            propiedades_list = [{"nombre": v['propiedad']} for v in vinculos]
            filtro_general.append({
                "id": clase.pk,
                "idclase": clase.idclase,
                "clase": clase.nombre,
                "propiedades": propiedades_list
            })
        
        marcas = Marca.objects.all()

        # Obtener todos los modelos con su idmarca
        modelos = Tblmodelo.objects.all()

        # Crear la lista de marcas
        lista_marcas = [
            {"id": marca.id, "nombre": marca.nombre}
            for marca in marcas
        ]
        filtro_general.append({"marcas": lista_marcas})

        # Crear la lista de modelos
        lista_modelos = [
            {"idmodelo": modelo.id, "nombre": modelo.nombre, "idmarca": modelo.idmarca.id if modelo.idmarca else None}
            for modelo in modelos
        ]
        
        filtro_general.append({"modelos": lista_modelos})
      
            
            
        # "filtro dinamico"
        filtro_dinamico = {
            "ancho": [],
            "perfil": [],
            "aro": []
        }
        
        

        # 1. Obtener todos los diferentes valores de ancho
        anchos = Tblitem.objects.filter(activo=True).values('ancho').annotate(
            items_existentes=Count('idproduct')
        ).order_by('ancho')
        filtro_dinamico['ancho'] = [
            {"ancho": a['ancho'], "items_existentes": a['items_existentes']}
            for a in anchos if a['ancho'] is not None
        ]

        # 2. Si se recibe "ancho", filtrar items por "ancho" y listar perfiles
# 2. Si se recibe "ancho", filtrar items por "ancho" y listar perfiles
        if "ancho" in filtros:
            ancho_filtro = filtros['ancho']
            items_por_ancho = Tblitem.objects.filter(activo=True, ancho=ancho_filtro)

                # Contar perfiles vinculados
            perfiles_vinculados = (
                items_por_ancho
                .prefetch_related('clases_propiedades')  # Traer todas las clases relacionadas
                .filter(clases_propiedades__idclase__nombre="Perfil")  # Filtrar solo las clases "Perfil"
                .values('clases_propiedades__propiedad')
                .annotate(items_existentes=Count('idproduct'))
                .order_by('clases_propiedades__propiedad')
            )

            # Construir el listado para filtro_dinamico
            filtro_dinamico['perfil'] = [
                {
                    "perfil": p['clases_propiedades__propiedad'],
                    "items_existentes": p['items_existentes']
                }
                for p in perfiles_vinculados if p['clases_propiedades__propiedad'] is not None
            ]
        
# 3. Si se reciben "ancho" y "perfil", filtrar items por ambos y listar aros
        if "ancho" in filtros and "perfil" in filtros:
            perfil_filtro = filtros['perfil']
            
            # Filtrar ítems por "ancho" y "perfil"
            items_por_ancho_y_perfil = Tblitem.objects.filter(
                activo=True,
                ancho=ancho_filtro,
                clases_propiedades__idclase__nombre="Perfil",  # Filtrar solo las clases "Perfil"
                clases_propiedades__propiedad=perfil_filtro  # Filtrar por el perfil recibido
            )

            # Filtrar los aros relacionados con los ítems filtrados por "ancho" y "perfil"
            aros = items_por_ancho_y_perfil.prefetch_related('clases_propiedades')  # Usar el queryset filtrado
            aros = aros.filter(clases_propiedades__idclase__nombre="Aro")  # Asegurarse de que solo se filtren los aros
            aros = aros.values('clases_propiedades__propiedad').annotate(
                items_existentes=Count('idproduct')
            ).order_by('clases_propiedades__propiedad')
            
            filtro_dinamico['aro'] = [
                {"aro": a['clases_propiedades__propiedad'], "items_existentes": a['items_existentes']}
                for a in aros if a['clases_propiedades__propiedad'] is not None
            ]

        # Respuesta final
        return Response({
            "filtro general": filtro_general,
            "filtro dinamico": filtro_dinamico
        })
    
from rest_framework.pagination import PageNumberPagination

class FixedPageNumberPagination(PageNumberPagination):
    page_size = 10  # Fijamos el tamaño de página a 10
from rest_framework.response import Response

class BusquedaDinamicaViewSet(viewsets.ViewSet):
    serializer_class = TblitemSerializer
    pagination_class = FixedPageNumberPagination  # Clase de paginación personalizada

    def create(self, request):
        # Obtener el JSON del cuerpo de la solicitud
        data = request.data
        params = request.query_params
        # Construcción del query
        query = Q()

        # Filtros adicionales opcionales
        # Filtros adicionales opcionales
        cadena_busqueda = data.get("cadena_busqueda")
        id_categoria = data.get("id_categoria")
        id_marca_list = data.get("id_marca", [])
        id_modelo_list = data.get("id_modelo", [])
        clase_categoria = data.get("clase_categoria", [])

        # Aplicar los filtros si están presentes
        if id_categoria:
            query &= Q(categoria_relacionada=id_categoria)

        if cadena_busqueda:
            query &= Q(titulo__icontains=cadena_busqueda)

        if id_marca_list:
            query &= Q(idmodelo__idmarca_id__in=id_marca_list)

        if id_modelo_list:
            query &= Q(idmodelo__in=id_modelo_list)

        if clase_categoria:
            subquery = Q()
            for item in clase_categoria:
                id_clase = item.get("id_clase")
                propiedad_list = item.get("propiedad", [])

                if id_clase and propiedad_list:
                    subquery |= Q(
                        clases_propiedades__idclase=id_clase,
                        clases_propiedades__propiedad__in=propiedad_list
                    )
            query &= subquery

        # Si no se envía ningún filtro, listar todos los items
        if not (id_categoria or cadena_busqueda or id_marca_list or id_modelo_list or clase_categoria):
            items = Tblitem.objects.all()
        else:
            # Filtrar los elementos que cumplen con los filtros
            items = Tblitem.objects.filter(query).distinct()

        ordering = params.get("ordering", None)
        if ordering:
            items = items.order_by(*ordering.split(","))
        

        ordering = params.get("ordering", None)
        print(ordering)
        if ordering:
            items = items.order_by(*ordering.split(","))
        # Paginación
        paginator = self.pagination_class()
        paginated_items = paginator.paginate_queryset(items, request)

        # Serializar los resultados
        serializer = TblitemSerializer(paginated_items, many=True)

        # Responder con los datos paginados
        return paginator.get_paginated_response(serializer.data)

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

class UserPedidosView(ModelViewSet):
    """
    ViewSet para manejar pedidos con soporte para búsquedas, filtros y ordenamiento.
    """
    permission_classes = [IsAuthenticated]
    #queryset = Tblpedido.objects.filter(activo=True).order_by('pk')  # Filtra solo pedidos activos
    serializer_class = TblpedidoSerializer

    # Configuración de filtros, búsquedas y ordenamiento
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['idcliente__nombreusuario', 'total', 'estado']
 # Permite ordenar por fecha o precio
    filterset_class = TblpedidoFilter  # Usar un filtro personalizado

    def get_queryset(self):
        # Filtrar los pedidos por el usuario autenticado
        user = self.request.user
        return Tblpedido.objects.filter(idcliente=user, activo=True).order_by('pk')
        
      
    
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
    queryset = Administracion.objects.filter(activo=True).order_by('pk')
    serializer_class = AdministracionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nombreempresa', 'ruc', 'telefono', 'idmoneda__nombre']
    filterset_fields = ['activo', 'nombreempresa', 'ruc', 'telefono', 'igv', 'idmoneda_id', 'idmoneda__nombre', 'fechacreacion', 'fechamodificacion']



class CuponViewSet(ModelViewSet):
    queryset = Cupon.objects.filter(activo=True).order_by('pk')
    serializer_class = CuponSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['descripcion', 'estado', 'fechavigencia']
    filterset_fields = {
    'activo': ['exact'],
    'idcupon': ['exact'],
    'cantidaddescuento': ['exact'],
    'estado': ['exact'],
    'fechavigencia': ['exact'],
    'fechacreacion': ['exact'],
    'fechamodificacion': ['exact'],
    'codigo': ['exact'],  # Búsqueda literal
}
class MarcaViewSet(ModelViewSet):
    queryset = Marca.objects.filter(activo=True).order_by('pk')
    serializer_class = MarcaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nombre']
    filterset_fields = ['activo', 'id', 'nombre']


class TblreclamacionViewSet(ModelViewSet):
    queryset = Tblreclamacion.objects.filter(activo=True).order_by('pk')
    serializer_class = TblreclaisionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nombre']
    filterset_fields = '__all__'



class MarcaViewSet(ModelViewSet):
    queryset = Marca.objects.filter(activo=True).order_by('pk')
    serializer_class = MarcaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nombre']
    filterset_fields = ['activo', 'id', 'nombre']

class TblcategoriaViewSet(ModelViewSet):
    queryset = Tblcategoria.objects.filter(activo=True).order_by('pk')
    serializer_class = TblcategoriaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nombre']
    filterset_fields = ['activo', 'id', 'nombre']

class FleteViewSet(ModelViewSet):
    queryset = Flete.objects.filter(activo=True).order_by('pk')
    serializer_class = FleteSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['iddepartamento',"idcategoria__nombre"]
    filterset_fields = ['precio','activo', 'id','idcategoria_id', 'idcategoria__nombre',"iddepartamento"]

    @action(detail=False, methods=['put'], url_path='matriz-update', serializer_class=DepartamentoSerializer)
    def matriz_actualizacion(self, request, *args, **kwargs):
        """
        Actualizar los registros de un departamento.
        """
        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            # Actualizar registros
            for departamento_data in serializer.validated_data:
                iddepartamento = departamento_data['iddepartamento']
                valores = departamento_data['valores']

                # Eliminar registros existentes del departamento
                Flete.objects.filter(iddepartamento=iddepartamento).delete()

                # Crear nuevos registros
                fletes = [
                    Flete(
                        iddepartamento=iddepartamento,
                        idcategoria_id=valor['idcategoria'],
                        precio=valor['val']
                    )
                    for valor in valores
                ]
                Flete.objects.bulk_create(fletes)

            return Response({'message': 'Fletes actualizados exitosamente.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='matriz-lista')
    def matriz_lista(self, request, *args, **kwargs):
        """
        Listar los departamentos con sus categorías y precios.
        """
        departamentos = Flete.objects.values('iddepartamento').distinct()
        data = []

        for departamento in departamentos:
            iddepartamento = departamento['iddepartamento']
            valores = Flete.objects.filter(iddepartamento=iddepartamento).values(
                categoria=F('idcategoria__id'),
                val=F('precio')
            )
            data.append({
                'iddepartamento': iddepartamento,
                'valores': list(valores)
            })

        return Response(data, status=status.HTTP_200_OK)
    @swagger_auto_schema(
        operation_description="Creación masiva de Fletes",
        request_body=DepartamentoSerializer(many=True),
        responses={201: "Fletes creados exitosamente", 400: "Error en los datos proporcionados"}
    )
    @action(detail=False, methods=['post'], url_path='matriz-creacion', serializer_class=DepartamentoSerializer)
    def matriz_creacion(self, request):
        """
        Acción personalizada para crear múltiples registros de Flete.
        """
        serializer = DepartamentoSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()  # Llama al método `create` en el serializer
            return Response({'message': 'Fletes creados exitosamente.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TblmodeloViewSet(ModelViewSet):
    queryset = Tblmodelo.objects.filter(activo=True).order_by('pk')
    serializer_class = TblmodeloSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nombre']
    filterset_fields = ['activo', 'id', 'nombre', 'idmarca_id']




class MonedaViewSet(ModelViewSet):
    queryset = Moneda.objects.filter(activo=True).order_by('pk')
    serializer_class = MonedaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nombre']
    filterset_fields = ['activo', 'idmoneda', 'nombre', 'estado', 'fechacreacion', 'fechamodificacion']



class PromocionViewSet(ModelViewSet):
    queryset = Promocion.objects.filter(activo=True).order_by('pk')
    serializer_class = PromocionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = [ 'estado']
    filterset_fields = ['activo', 'idpromocion', 'estado', 'fechacreacion', 'fechamodificacion']


class TblcarritoViewSet(ModelViewSet):
    queryset = Tblcarrito.objects.filter(activo=True).order_by('pk')
    serializer_class = TblcarritoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['idusuario__nombreusuario', 'preciototal']
    filterset_fields = ['activo', 'idusuario_id', 'preciototal']



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from requests.auth import HTTPBasicAuth
import base64
class AuthCredentialsView(APIView):
    """
    Servicio para generar el encabezado 'Authorization' con la autenticación básica.
    """

    def get(self, request, *args, **kwargs):
        # Obtener las credenciales desde la configuración de Django o desde los parámetros
        username = settings.IZIPAY_USERNAME  # O puedes recibirlo como parámetro en la URL si es necesario
        password = settings.IZIPAY_PASSWORD  # O puedes recibirlo como parámetro también

        # Concatenar el nombre de usuario y la contraseña con un ':' entre ellos
        user_pass_string = f"{username}:{password}"

        # Codificar en base64
        base64_encoded = base64.b64encode(user_pass_string.encode('utf-8')).decode('utf-8')

        # Construir el encabezado de autorización
        auth_header = f"Basic {base64_encoded}"

        # Retornar la respuesta con el encabezado generado
        return Response(
            data={
                "authorization_header": auth_header
            },
            status=status.HTTP_200_OK
        )

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from .models import Tblitem
from .serializers import TblitemSerializer
from .filters import TblitemclasepropiedadFilter
from .filters import *
from rest_framework import filters


from django.db import transaction
from django.core.exceptions import ValidationError
from django.db.models import Sum, F, DecimalField
from django.utils.timezone import now 

class TblitemViewSet(ModelViewSet):
    queryset = Tblitem.objects.prefetch_related(
        'clases_propiedades',
        'clases_propiedades__idclase'
        # 'clases_propiedades__propiedad'
    ).all()
    serializer_class = TblitemSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, DateTimeIntervalFilter]
    filterset_class = TblitemFilter
  
    #----------------------------------------------------------------
    @action(detail=False, methods=['get'], url_path='filtrobusqueda')
    def busqueda_dinamicaitems(self, request):
        """
        Acción personalizada para realizar búsquedas dinámicas con filtros adicionales.
        """
        data = request.query_params
        query = Q()

        # Filtros adicionales opcionales
        cadena_busqueda = data.get("cadena_busqueda")
        id_categoria = data.get("id_categoria")
        id_marca_list = data.getlist("id_marca", [])
        id_modelo_list = data.getlist("id_modelo", [])
        clase_categoria = data.getlist("clase_categoria", [])

        # Aplicar los filtros si están presentes
        if id_categoria:
            query &= Q(categoria_relacionada=id_categoria)

        if cadena_busqueda:
            query &= Q(titulo__icontains=cadena_busqueda)

        if id_marca_list:
            query &= Q(idmodelo__idmarca_id__in=id_marca_list)

        if id_modelo_list:
            query &= Q(idmodelo__in=id_modelo_list)

        if clase_categoria:
            subquery = Q()
            for item in clase_categoria:
                id_clase = item.get("id_clase")
                propiedad_list = item.get("propiedad", [])

                if id_clase and propiedad_list:
                    subquery |= Q(
                        clases_propiedades__idclase=id_clase,
                        clases_propiedades__propiedad__in=propiedad_list
                    )
            query &= subquery

        # Obtener queryset filtrado
        items = Tblitem.objects.filter(query).distinct()
        
         # Aplicar ordenamiento manual
        ordering = data.get("ordering")
        if ordering:
            items = items.order_by(*ordering.split(","))
            
        # Serializar los resultados (la paginación y el ordenamiento se aplicarán automáticamente)
        paginator = self.pagination_class()
        paginated_items = paginator.paginate_queryset(items, request, view=self)

        # Serializar los resultados
        serializer = self.get_serializer(paginated_items, many=True)

        # Responder con los datos paginados
        return paginator.get_paginated_response(serializer.data)
    #----------------------------------------------------------------

    @swagger_auto_schema(
        operation_description="Obtiene el detalle completo del ítem junto con el número de pedidos y los ingresos totales.",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "item_data": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            #**{
                            #    field: serializer_field.schema for field, serializer_field in TblitemSerializer().fields.items()
                            #},
                            "numero_pedidos": openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description="Número total de pedidos en los que aparece este producto."
                            ),
                            "ingresos_totales": openapi.Schema(
                                type=openapi.TYPE_NUMBER,
                                format=openapi.FORMAT_DECIMAL,
                                description="Ingresos totales generados por este producto (suma del precio unitario multiplicado por la cantidad)."
                            ),
                        },
                    ),
                },
            ),
            404: openapi.Response('Error: El ítem no existe.'),
        },
    )
    @action(detail=True, methods=['get'], url_path='detalles-ventas')
    def detalles_ventas(self, request, pk=None):
        """
        Obtiene el detalle completo del ítem junto con el número de pedidos y los ingresos totales.
        """
        try:
            item = Tblitem.objects.get(pk=pk)
        except Tblitem.DoesNotExist:
            return Response({'error': 'El ítem no existe.'}, status=404)

        # Filtrar los pedidos que incluyen este ítem
        detalles_pedidos = Tbldetallepedido.objects.filter(idproduct=item)

        # Cálculo del número de pedidos y los ingresos totales
        numero_pedidos = detalles_pedidos.count()
        ingresos_totales = detalles_pedidos.aggregate(
            total_ingresos=Sum(F('cantidad') * F('preciunitario'), output_field=DecimalField())
        )['total_ingresos'] or 0

        # Serializar el detalle del ítem
        item_data = self.get_serializer(item).data

        # Agregar información adicional
        item_data.update({
            'numero_pedidos': numero_pedidos,
            'ingresos_totales': ingresos_totales,
        })

        return Response(item_data)
    
    
    #----------------------------------------------------------------
  
    @action(detail=True, methods=['patch'], url_path='update', serializer_class=TblitemTestSerializer)
    @transaction.atomic
    def itempartial_update(self, request, pk=None):
        """
        Actualiza parcialmente un item identificado por su ID en el URL.
        """
        
        try:
            # Obtener el item por medio del ID en el URL
            item = Tblitem.objects.get(pk=pk)
            
        except Tblitem.DoesNotExist:
            return Response({"error": "El item no existe."}, status=status.HTTP_404_NOT_FOUND)
            

        # Validar los datos enviados (parciales)
        serializer = self.get_serializer(item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        

        try:
            with transaction.atomic():
                # Actualizar campos proporcionados
                item_data = validated_data.get('item', {})
                for key, value in item_data.items():
                    setattr(item, key, value)
                item.save()

                # Actualizar relaciones selectivamente
                if 'vinculos' in validated_data:
                    self.patch_item_vinculos(item, json.loads(validated_data.get('vinculos', '[]')))
                if 'categorias' in validated_data:
                    cate= json.loads(validated_data.get('categorias', '[]'))
                    self.patch_item_categorias(item, cate)
                if 'cupones' in validated_data:
                    self.patch_item_cupones(item, json.loads(validated_data.get('cupones', '[]')))
                if 'itemsrelacionados' in validated_data:

                    self.patch_item_itemsrelacionados(item, json.loads(validated_data.get('itemsrelacionados', '[]')))

                # Actualizar imágenes principales y adicionales
                if 'imagenprincipal' in validated_data:
                    item.imagenprincipal = validated_data['imagenprincipal']
                    item.save()
                
                if 'idmodelo' in validated_data:
                    try:
                        modelo_instance = Tblmodelo.objects.get(id=validated_data['idmodelo'])
                        item.idmodelo = modelo_instance # Asignar la instancia de Tblmodelo
                    except Tblmodelo.DoesNotExist:
                        raise ValueError(f"El modelo con ID {item_data['idmodelo']} no existe.") # Asignar la imagen principal


                if 'imagenes_eliminartodas' in validated_data and validated_data['imagenes_eliminartodas']:
    # Caso 1: Si se especifica `imagenes_eliminartodas=True`, eliminar todas las imágenes
                    Tblimagenitem.objects.filter(idproduct=item).delete()

                elif 'imagenes' in validated_data:
                    imagenes_data = validated_data.get('imagenes', [])

                    if imagenes_data:
                        # Caso 2: Si `imagenes` contiene imágenes, eliminar las existentes y añadir las nuevas
                        Tblimagenitem.objects.filter(idproduct=item).delete()
                        for imagen in imagenes_data:
                            if imagen:  # Verifica que la imagen no esté vacía
                                Tblimagenitem.objects.create(
                                    idproduct=item,
                                    imagen=imagen,
                                    estado=1  # Ajusta según la lógica de tu modelo
                                )
                    else:
                        # Caso 3: Si `imagenes` está presente pero vacío, no hacer nada
                        pass

                # Serializar y responder
                item_serializer = TblitemSerializer(item)
                return Response({
                    "message": "Item actualizado parcialmente con éxito.",
                    "item": item_serializer.data
                }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Error inesperado: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def patch_item_vinculos(self, item, vinculos_data):
        """
        Actualiza los vínculos asociados a un ítem de forma parcial.
        Elimina los vínculos existentes que no están en los datos enviados.
        """
        # Obtener las relaciones actuales desde la base de datos
        relaciones_actuales = tblitemclasevinculo.objects.filter(iditem=item)
        relaciones_por_id = {rel.id: rel for rel in relaciones_actuales}
        relaciones_por_clase = {rel.idclase_id: rel for rel in relaciones_actuales}

        # Rastrear los vínculos que deben conservarse
        vinculos_a_conservar = set()

        for vinculo in vinculos_data:
            if 'id' in vinculo:  # Relación existente enviada por ID
                if vinculo['id'] in relaciones_por_id:
                    relacion = relaciones_por_id[vinculo['id']]
                    # Actualizar solo si los datos han cambiado
                    if relacion.idclase_id != vinculo.get('idclase') or relacion.propiedad != vinculo.get('propiedad'):
                        relacion.idclase_id = vinculo.get('idclase', relacion.idclase_id)
                        relacion.propiedad = vinculo.get('propiedad', relacion.propiedad)
                        relacion.save()
                    vinculos_a_conservar.add(relacion.id)

            elif 'idclase' in vinculo:  # Relación nueva o existente enviada por clase
                if vinculo['idclase'] in relaciones_por_clase:
                    relacion = relaciones_por_clase[vinculo['idclase']]
                    # Actualizar la propiedad si es necesario
                    if relacion.propiedad != vinculo.get('propiedad', relacion.propiedad):
                        relacion.propiedad = vinculo.get('propiedad', relacion.propiedad)
                        relacion.save()
                    vinculos_a_conservar.add(relacion.id)
                else:  # Crear una nueva relación
                    nueva_relacion = tblitemclasevinculo.objects.create(
                        iditem=item,
                        idclase_id=vinculo['idclase'],
                        propiedad=vinculo.get('propiedad', "")
                    )
                    vinculos_a_conservar.add(nueva_relacion.id)

        # Eliminar vínculos no enviados
        relaciones_actuales.exclude(id__in=vinculos_a_conservar).delete()


    def patch_item_categorias(self, item, categorias_data):
        """
        Actualiza las categorías asociadas a un ítem de forma parcial.
        Elimina las relaciones existentes que no están en los datos enviados.
        """
        # Obtener las relaciones actuales desde la base de datos
        relaciones_actuales = tblitemcategoria.objects.filter(iditem=item)
        relaciones_por_id = {rel.id: rel for rel in relaciones_actuales}
        relaciones_por_categoria = {rel.idcategoria_id: rel for rel in relaciones_actuales}

        # Rastrear las relaciones que deben conservarse
        categorias_a_conservar = set()

        for categoria in categorias_data:
            if 'id' in categoria:  # Relación existente enviada por ID
                if categoria['id'] in relaciones_por_id:
                    relacion = relaciones_por_id[categoria['id']]
                    # Actualizar solo si los datos han cambiado
                    if relacion.idcategoria_id != categoria.get('idcategoria'):
                        relacion.idcategoria_id = categoria.get('idcategoria')
                        relacion.save()
                    categorias_a_conservar.add(relacion.id)

            elif 'idcategoria' in categoria:  # Relación nueva o existente enviada por categoría
                if categoria['idcategoria'] in relaciones_por_categoria:
                    relacion = relaciones_por_categoria[categoria['idcategoria']]
                    categorias_a_conservar.add(relacion.id)
                else:
                    nueva_relacion = tblitemcategoria.objects.create(
                        iditem=item,
                        idcategoria_id=categoria['idcategoria']
                    )
                    categorias_a_conservar.add(nueva_relacion.id)
        
        # Eliminar relaciones no enviadas
        relaciones_actuales.exclude(id__in=categorias_a_conservar).delete()


    def patch_item_cupones(self, item, cupones_data):
        """
        Actualiza los cupones asociados a un ítem de forma parcial.
        Elimina las relaciones existentes que no están en los datos enviados.
        """
        # Obtener las relaciones actuales desde la base de datos
        relaciones_actuales = tblitemcupon.objects.filter(iditem=item)
        relaciones_por_id = {rel.id: rel for rel in relaciones_actuales}
        relaciones_por_cupon = {rel.idcupon_id: rel for rel in relaciones_actuales}

        # Rastrear las relaciones que deben conservarse
        cupones_a_conservar = set()

        for cupon in cupones_data:
            if 'id' in cupon:  # Relación existente enviada por ID
                if cupon['id'] in relaciones_por_id:
                    relacion = relaciones_por_id[cupon['id']]
                    # Actualizar solo si los datos han cambiado
                    if relacion.idcupon_id != cupon.get('idcupon'):
                        relacion.idcupon_id = cupon.get('idcupon')
                        relacion.save()
                    cupones_a_conservar.add(relacion.id)

            elif 'idcupon' in cupon:  # Relación nueva o existente enviada por cupón
                if cupon['idcupon'] in relaciones_por_cupon:
                    relacion = relaciones_por_cupon[cupon['idcupon']]
                    cupones_a_conservar.add(relacion.id)
                else:
                    nueva_relacion = tblitemcupon.objects.create(
                        iditem=item,
                        idcupon_id=cupon['idcupon']
                    )
                    cupones_a_conservar.add(nueva_relacion.id)

        # Eliminar relaciones no enviadas
        relaciones_actuales.exclude(id__in=cupones_a_conservar).delete()


    def patch_item_itemsrelacionados(self, item, itemsrelacionados_data):
        """
        Actualiza los ítems relacionados asociados a un ítem de forma parcial.
        Elimina las relaciones existentes que no están en los datos enviados.
        """
        # Obtener las relaciones actuales desde la base de datos
        relaciones_actuales = Tblitemrelacionado.objects.filter(item=item)
        relaciones_por_id = {rel.id: rel for rel in relaciones_actuales}
        relaciones_por_item_relacionado = {rel.item_relacionado_id: rel for rel in relaciones_actuales}

        # Rastrear las relaciones que deben conservarse
        itemsrelacionados_a_conservar = set()

        for itemsrelacionados in itemsrelacionados_data:
            if 'id' in itemsrelacionados:  # Relación existente enviada por ID
                if itemsrelacionados['id'] in relaciones_por_id:
                    relacion = relaciones_por_id[itemsrelacionados['id']]
                    # Actualizar solo si los datos han cambiado
                    if relacion.item_relacionado_id != itemsrelacionados.get('item_relacionado'):
                        relacion.item_relacionado_id = itemsrelacionados.get('item_relacionado')
                        relacion.save()
                    itemsrelacionados_a_conservar.add(relacion.id)

            elif 'item_relacionado' in itemsrelacionados:  # Relación nueva o existente enviada por ítem relacionado
                if itemsrelacionados['item_relacionado'] in relaciones_por_item_relacionado:
                    relacion = relaciones_por_item_relacionado[itemsrelacionados['item_relacionado']]
                    itemsrelacionados_a_conservar.add(relacion.id)
                else:
                    nuevo_relacionado = Tblitemrelacionado.objects.create(
                        item=item,
                        item_relacionado_id=itemsrelacionados['item_relacionado']
                    )
                    itemsrelacionados_a_conservar.add(nuevo_relacionado.id)

        # Eliminar relaciones no enviadas
        relaciones_actuales.exclude(id__in=itemsrelacionados_a_conservar).delete()

  
    #---------
    @action(detail=False, methods=['post'], url_path='upload-multiple', serializer_class=TblitemTestSerializer)
    @transaction.atomic
    def upload_multiple(self, request):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        # Desempaqueta los datos de entrada
        item_data = validated_data.get('item', {})
        vinculos_data = json.loads(validated_data.get('vinculos', '[]'))
        categorias_data = json.loads(validated_data.get('categorias', '[]'))
        cupones_data = json.loads(validated_data.get('cupones', '[]'))
        itemsrelacionados_data = json.loads(validated_data.get('itemsrelacionados', '[]'))
        imagenes_data = validated_data.get('imagenes', [])
        imagen_principal = validated_data.get('imagenprincipal', None)  # Asignado el campo 'imagenprincipal' para la imagen principal
        idmodelo = validated_data.get('idmodelo', None)  # Asignado el campo 'imagenprincipal' para la imagen principal

        try:
            with transaction.atomic():
                # Crear el item y manejar relaciones
                item_data_dict = item_data.copy()  # Hacer una copia para agregar la imagen principal

                # Si hay una imagen principal, agregarla a los datos del item
                if imagen_principal:
                    item_data_dict['imagenprincipal'] = imagen_principal  # Asignar la imagen principal
                if idmodelo:
                    try:
                        modelo_instance = Tblmodelo.objects.get(id=idmodelo)
                        item_data_dict['idmodelo'] = modelo_instance  # Asignar la instancia de Tblmodelo
                    except Tblmodelo.DoesNotExist:
                        raise ValueError(f"El modelo con ID {item_data_dict['idmodelo']} no existe.") # Asignar la imagen principal

                # Crear el item con los datos (incluyendo imagen principal)
                item = self.create_item_with_vinculos(item_data_dict, vinculos_data)
                self.create_item_categorias(item, categorias_data)
                self.create_item_cupones(item, cupones_data)
                self.create_item_itemsrelacionados(item, itemsrelacionados_data)

                # Procesar imágenes adicionales
                for imagen in imagenes_data:
                    Tblimagenitem.objects.create(
                        idproduct=item,
                        imagen=imagen,
                        estado=1  # Ajusta según tu lógica
                    )

                # Serializa el item creado (usando el serializer correcto para la respuesta)
                item_serializer = TblitemSerializer(item)

                return Response({
                    "message": "Item creado con éxito.",
                    "item": item_serializer.data,  # Serializa el item recién creado
                }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"Error inesperado: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    def create_item_with_vinculos(self, item_data, vinculos_data):
        """
        Crea un item y sus vínculos asociados en una operación atómica.
        """
        # Crear el item
        item = Tblitem.objects.create(**item_data)

        # Crear los vínculos asociados
        vinculos = [
            tblitemclasevinculo(
                iditem=item,
                idclase_id=vinculo.get("idclase"),
                propiedad=vinculo.get("propiedad", "")
            )
            for vinculo in vinculos_data
        ]
        tblitemclasevinculo.objects.bulk_create(vinculos)

        return item
    def create_item_categorias(self, item, categorias_data):
        """
        Crea las categorías asociadas a un item.
        """
        # Crear las categorías asociadas
        categorias = [
            tblitemcategoria(
                iditem=item,
                idcategoria_id=categoria.get("idcategoria")
            )
            for categoria in categorias_data
        ]
        tblitemcategoria.objects.bulk_create(categorias)


        
    def create_item_cupones(self, item, cupones_data):
        """
        Crea los cupones asociados a un item.
        """
        # Crear los cupones asociados
        cupones = [
            tblitemcupon(
                iditem=item,
                idcupon_id=cupon.get("idcupon")
            )
            for cupon in cupones_data
        ]
        tblitemcupon.objects.bulk_create(cupones)
        
    def create_item_itemsrelacionados(self, item, itemsrelacionados_data):
        """
        Crea los items relacionados a un item.
        """
        # Crear los items relacionados asociados
        items_relacionados = [
            Tblitemrelacionado(
                item=item,
                item_relacionado_id=itemsrelacionados.get("item_relacionado")  # Asegúrate de usar _id si es un ForeignKey
            )
            for itemsrelacionados in itemsrelacionados_data  # Itera correctamente sobre los datos
        ]
        
        # Crear en masa los registros de relaciones
        Tblitemrelacionado.objects.bulk_create(items_relacionados)

    @action(detail=False, methods=['post'], url_path='bulk-upload')
    @transaction.atomic
    def bulk_upload(self, request):
        """
        Carga masiva de productos desde un archivo Excel con validación de dependencias entre marca y modelo.
        """
        try:
            # Verifica si hay un archivo en la solicitud
            file = request.FILES.get('file')
            if not file:
                return Response({"error": "No se ha proporcionado ningún archivo."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Leer el archivo Excel (saltando la primera fila de encabezados)
            df = pd.read_excel(file, header=1)

            # Validar que las columnas requeridas existan
            required_columns = ["CODIGO(SKU)", "NOMBRE DEL PRODUCTO", "STOCK", "PRECIO", "MARCA", "MODELO"]
            for column in required_columns:
                if column not in df.columns:
                    return Response(
                        {"error": f"Falta la columna requerida: {column}"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            # Procesar cada fila
            errors = []
            created_or_updated_items = []
            for index, row in df.iterrows():
                try:
                    # Extraer datos
                    sku = row["CODIGO(SKU)"]
                    titulo = row["NOMBRE DEL PRODUCTO"]
                    stock = row["STOCK"]
                    precio_normal = row["PRECIO"]
                    marca_id = row["MARCA"]
                    modelo_id = row["MODELO"]
                    ancho = row.get("ANCHO", None)
                    categoria_id = row.get("CATEGORIA", None)  # ID de la categoría

                    # Validar datos mínimos
                    if not sku or not titulo or not marca_id or not modelo_id:
                        raise ValueError("SKU, Título, Marca y Modelo son obligatorios.")

                    # Validar que la marca existemarc
                    
                    try:
                        marca_instance = Marca.objects.get(id=marca_id)
                    except Marca.DoesNotExist:
                        raise ValueError(f"La marca con ID {marca_id} no existe.")

                    # Validar que el modelo existe y pertenece a la marca
                    try:
                        modelo_instance = Tblmodelo.objects.get(id=modelo_id, idmarca=marca_id)
                    except Tblmodelo.DoesNotExist:
                        raise ValueError(
                            f"El modelo con ID {modelo_id} no existe o no pertenece a la marca con ID {marca_id}."
                        )
                    try:
                        categoria_instance = Tblcategoria.objects.get(id=categoria_id)
                    except Tblcategoria.DoesNotExist:
                        raise ValueError(f"La categoría con ID {categoria_id} no existe.")
                    
                    otros_datos = {
                                "ancho": ancho,
                            }
                    # Crear o actualizar el producto
                    item, created =  Tblitem.objects.update_or_create(
                        codigosku=sku,
                        defaults={
                            "titulo": titulo,
                            "stock": stock,
                            "precionormal": precio_normal,
                            "ancho": ancho,
                            "fechapublicacion": row.get("FECHA PUBLICACION") or now(),
                            "destacado": True,
                            "nuevoproducto": False,
                            "estado": 1,
                            "idmodelo": modelo_instance,  # Asignar el modelo validado
                            **otros_datos,
                        },
                    )
                    
                    item.categoria_relacionada.all().delete()  # Limpiar categorías existentes
                    tblitemcategoria.objects.create(iditem=item, idcategoria=categoria_instance)

                    vinculos_data = {
                                "PLIEGUES": row.get("PLIEGUES", None),
                                "IC_IV": row.get("IC/IV", None),
                                "APLICACION": row.get("APLICACIÓN", None),
                                "SERVICIO": row.get("SERVICIO", None),
                                "ARO": row.get("ARO", None),
                                "ARO_PERMITIDO": row.get("ARO PERMITIDO", None),
                                "PERFIL": row.get("PERFIL", None),
                                "PRESENTACION": row.get("PRESENTACION", None),
                                "RANGO_VELOCIDAD": row.get("RANGO VELOCIDAD", None),
                                "RUNFLAT": row.get("RUNFLAT", None),
                                "INDICE_CARGA": row.get("INDICE DE CARGA", None),
                            }
                    
        # Crear nuevos vínculos
                    for key, value in vinculos_data.items():
                        if value:
                            # Buscar la clase por nombre
                            clase_instance, _ = Tblitemclase.objects.get_or_create(
                                nombre=key,
                                defaults={"activo": True},
                            )
                            # Crear o actualizar el vínculo
                            tblitemclasevinculo.objects.update_or_create(
                                iditem=item,
                                idclase=clase_instance,
                                defaults={
                                    "propiedad": value,
                                    "activo": True,
                                },
                            )
                    # Agregar el producto creado o actualizado a la lista
                    created_or_updated_items.append(item)

                except Exception as e:
                    # Registrar errores por fila
                    errors.append({
                        "fila": index + 3,  # +3 porque pandas usa 0-index y hay dos encabezados
                        "sku": row.get("CODIGO(SKU)", "Desconocido"),
                        "error": str(e),
                    })

            # Responder con éxito parcial o total
            if errors:
                return Response(
                    {
                        "message": "Carga masiva completada con errores.",
                        "errors": errors,
                        "items": TblitemSerializer(created_or_updated_items, many=True).data,
                    },
                    status=status.HTTP_207_MULTI_STATUS,
                )

            return Response({
                "message": "Carga masiva completada con éxito.",
                "items": TblitemSerializer(created_or_updated_items, many=True).data,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Error inesperado: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='download-template')
    def download_template(self, request):
        """
        Descarga la plantilla para la carga masiva con dos cabeceras.
        """
        # Crear un DataFrame con las columnas requeridas
        columns = [
            "CODIGO(SKU)", "NOMBRE DEL PRODUCTO", "STOCK", "PRECIO", "MARCA",
            "MODELO", "CATEGORIA", "ANCHO", "PLIEGUES", "IC/IV", "APLICACIÓN",
            "SERVICIO", "ARO", "ARO PERMITIDO", "PERFIL", "PRESENTACION",
            "RANGO VELOCIDAD", "RUNFLAT", "INDICE DE CARGA"
        ]
        mandatory = [
            "SI", "SI", "SI", "SI", "NO",
            "NO", "NO", "NO", "NO", "NO",
            "NO", "NO", "NO", "NO", "NO",
            "NO", "NO", "NO", "NO"
        ]

        # Crear un DataFrame con las dos filas de encabezado
        df = pd.DataFrame([mandatory, columns])

        # Convertir el DataFrame a un archivo Excel
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="plantilla_carga_masiva.xlsx"'
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, header=False, index=False, sheet_name="Plantilla")

        return response
#------------------------------------------------------------------
from rest_framework.parsers import MultiPartParser
import pandas as pd
from django.db import transaction
class BulkUploadItemsAPIView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get('file')

        if not file:
            return Response({"detail": "No se proporcionó ningún archivo."}, status=400)

        try:
            # Leer el archivo Excel
            df = pd.read_excel(file)
        except Exception as e:
            return Response({"detail": f"Error al leer el archivo: {str(e)}"}, status=400)

        required_columns = [
            'activo', 'codigosku', 'titulo', 'stock', 'descripcion', 'destacado',
            'agotado', 'nuevoproducto', 'preciorebajado', 'precionormal',
            'fechapublicacion', 'peso', 'altura', 'profundidad',
            'ancho', 'estado', 'idmodelo'
        ]

        # Verificar que todas las columnas requeridas estén presentes
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return Response({"detail": f"Faltan las siguientes columnas en el archivo: {', '.join(missing_columns)}"}, status=400)

        items_to_create = []

        for _, row in df.iterrows():
            try:
                item_data = {
                    'activo': row['activo'],
                    'codigosku': row['codigosku'],
                    'titulo': row['titulo'],
                    'stock': row['stock'],
                    'descripcion': row['descripcion'],
                    'destacado': row['destacado'],
                    'agotado': row.get('agotado', None),
                    'nuevoproducto': row['nuevoproducto'],
                    'preciorebajado': row.get('preciorebajado', None),
                    'precionormal': row['precionormal'],
                    'imagenprincipal': row.get('imagenprincipal', None),
                    'fechapublicacion': row['fechapublicacion'],
                    'peso': row.get('peso', None),
                    'altura': row.get('altura', None),
                    'profundidad': row.get('profundidad', None),
                    'ancho': row.get('ancho', None),
                    'estado': row['estado'],
                    'idmodelo_id': row.get('idmodelo', None),
                }
                
                # Validar con el serializer
                serializer = TblitemSerializer(data=item_data)
                serializer.is_valid(raise_exception=True)

                # Agregar a la lista de creación masiva
                items_to_create.append(Tblitem(**serializer.validated_data))

            except Exception as e:
                return Response({"detail": f"Error en la fila {_ + 2}: {str(e)}"}, status=400)

        # Crear los ítems en la base de datos
        try:
            with transaction.atomic():
                Tblitem.objects.bulk_create(items_to_create)
        except Exception as e:
            return Response({"detail": f"Error al guardar los datos: {str(e)}"}, status=500)

        return Response({"detail": "Items cargados exitosamente.", "total": len(items_to_create)})

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import Tblitem
from openpyxl import load_workbook
from django.db import transaction

def upload_xlsx(request):
    if request.method == "POST":
        file = request.FILES.get('file')
        if not file.name.endswith('.xlsx'):
            messages.error(request, "El archivo debe ser formato .xlsx")
            return redirect('upload_xlsx')

        try:
            wb = load_workbook(file)
            sheet = wb.active

            items_to_save = []
            for row in sheet.iter_rows(min_row=2, values_only=True):  # Asume que la primera fila tiene encabezados
                codigosku, titulo, stock, descripcion, destacado, agotado, nuevoproducto, precionormal, fechapublicacion = row[:9]
                
                item = Tblitem(
                    codigosku=codigosku,
                    titulo=titulo,
                    stock=stock,
                    descripcion=descripcion,
                    destacado=bool(destacado),
                    agotado=bool(agotado),
                    nuevoproducto=bool(nuevoproducto),
                    precionormal=precionormal,
                    fechapublicacion=fechapublicacion,
                    estado=1  # Suponiendo un valor predeterminado para estado
                )
                items_to_save.append(item)

            with transaction.atomic():
                Tblitem.objects.bulk_create(items_to_save)

            messages.success(request, "Datos subidos exitosamente.")
        except Exception as e:
            messages.error(request, f"Error al procesar el archivo: {e}")
        return redirect('upload_xlsx')

    return render(request, 'upload_xlsx.html')



def download_template(request):
    # Generar la plantilla
    wb = Workbook()
    ws = wb.active
    ws.title = "Plantilla"
    
    # Encabezados
    headers = [
        "codigosku", "titulo", "stock", "descripcion", 
        "destacado (1 o 0)", "agotado (1 o 0)", 
        "nuevoproducto (1 o 0)", "precionormal", "fechapublicacion (YYYY-MM-DD)"
    ]
    ws.append(headers)

    # Ejemplo de datos
    example_data = [
        "SKU001", "Producto A", 10, "Descripción A", 
        1, 0, 1, 100.00, "2024-01-01"
    ]
    ws.append(example_data)

    # Configurar la respuesta para descargar el archivo
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename=plantilla_items.xlsx'
    wb.save(response)
    return response





class TblnoticiaViewSet(ModelViewSet):
    queryset = Tblnoticia.objects.filter(activo=True).order_by('pk')
    serializer_class = TblnoticiaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['descripcion', 'estado']
    filterset_fields = ['activo', 'idnoticia', 'descripcion', 'estado', 'fechacreacion', 'fechamodificacion']


class TblsedeViewSet(ModelViewSet):
    queryset = Tblsede.objects.filter(activo=True).order_by('pk')
    serializer_class = TblsedeSerializer

class TblpedidoViewSet(ModelViewSet):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'sin_transaccion',
                openapi.IN_QUERY,
                description="Filtra los pedidos sin transacción asignada",
                type=openapi.TYPE_BOOLEAN
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    
    queryset = Tblpedido.objects.filter(activo=True).order_by('pk')
    serializer_class = TblpedidoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['idcliente__nombreusuario', 'total', 'estado']
    filterset_class = TblpedidoFilter
    def create(self, request, *args, **kwargs):
        """
        Sobrescribe el método create para procesar detalles del pedido.
        """
        data = request.data
        productos = data.pop('productos', None)  # Extraemos los productos del payload

        if not productos or not isinstance(productos, list):
            raise ValidationError({'productos': 'Debe incluir una lista de productos.'})
        
        with transaction.atomic():  # Usamos una transacción para garantizar consistencia
            pedido_serializer = self.get_serializer(data=data)
            pedido_serializer.is_valid(raise_exception=True)
            pedido = pedido_serializer.save()

            # Procesar los productos
            for producto in productos:
                producto['idpedido'] = pedido.idpedido  # Asociamos el pedido
                detalle_serializer = TbldetallepedidoSerializer(data=producto)
                detalle_serializer.is_valid(raise_exception=True)
                detalle_serializer.save()

        return Response(pedido_serializer.data, status=status.HTTP_201_CREATED)

class TblCarruselViewSet(ModelViewSet):
    queryset = TblCarrusel.objects.filter(activo=True).order_by('pk')
    serializer_class = TblCarruselSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['descripcion', 'estado']
    filterset_fields = ['activo', 'id',  'descripcion', 'estado', 'fechacreacion', 'fechamodificacion']



class TblusuarioViewSet(ModelViewSet):
    queryset = CustomUser.objects.filter(activo=True).order_by('pk')
    serializer_class = CustomUserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nombreusuario', 'nombre', 'apellidos', 'estado']
    filterset_fields = ['activo', 'nombreusuario', 'nombre', 'apellidos','departamento','provincia','distrito','telefono', 'estado', 'email_verified_at', 'direccion', 'fechacreacion', 'fechamodificacion','is_staff']



class TipocambioViewSet(ModelViewSet):
    queryset = Tipocambio.objects.filter(activo=True).order_by('pk')
    serializer_class = TipocambioSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['tipocambio', 'idmoneda__nombre', 'fechacreacion', 'fechamodificacion']
    filterset_fields = ['activo', 'tipocambio', 'idmoneda__nombre', 'fechacreacion', 'fechamodificacion']




class ValoracionViewSet(ModelViewSet):
    queryset = Valoracion.objects.filter(activo=True).order_by('pk')
    serializer_class = ValoracionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['comentario', 'estrellas']
    filterset_fields = ['activo', 'idvaloracion', 'estrellas', 'comentario', 'estado', 'idproduct_id', 'fechacreacion', 'fechamodificacion']

    


class TbldetallecarritoViewSet(ModelViewSet):
    queryset = Tbldetallecarrito.objects.filter(activo=True).order_by('pk')
    serializer_class = TbldetallecarritoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['idproduct__descripcion', 'cantidad']
    filterset_fields = ['activo',  'idproduct_id', 'cantidad', 'isuser_id', 'idcupon_id']

class TbldetallecarritoViewSet(ModelViewSet):
    queryset = Tbldetallecarrito.objects.filter(activo=True).order_by('pk')
    serializer_class = TbldetallecarritoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['idproduct__descripcion', 'cantidad']
    filterset_fields = ['activo',  'idproduct_id', 'cantidad', 'isuser_id', 'idcupon_id']



class TblimagenitemViewSet(ModelViewSet):
    queryset = Tblimagenitem.objects.filter(activo=True).order_by('pk')
    serializer_class = TblimagenitemSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['imagen', 'idproduct__descripcion']
    filterset_fields = ['activo', 'idimagen', 'idproduct_id', 'estado']
    
    @action(detail=False, methods=['post'], url_path='upload-multiple', serializer_class=MultipleImagenItemSerializer)
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
    queryset = Tblitemclase.objects.filter(activo=True).order_by('pk')
    serializer_class = TblitemclaseSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nombre']
    filterset_fields = ['activo', 'idclase', 'nombre']

class tblitemcuponSerializerViewSet(ModelViewSet):
    queryset = tblitemcupon.objects.filter(activo=True).order_by('pk')
    serializer_class = tblitemcuponSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nombre']
    filterset_fields = ['activo', 'id', 'iditem_id', 'idcupon_id']



class tblitemclasevinculoViewSet(ModelViewSet):
    queryset = tblitemclasevinculo.objects.filter(activo=True).order_by('pk')
    serializer_class = TblitemclasevinculoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = [ 'propiedad', 'idclase__nombre']
    filterset_fields = ['activo', 'id', 'iditem_id', 'propiedad', 'idclase_id']



class TblitempropiedadViewSet(ModelViewSet):
    queryset = Tblitempropiedad.objects.filter(activo=True).order_by('pk')
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
    queryset = Tblitemrelacionado.objects.filter(activo=True).order_by('pk')
    serializer_class = TblitemrelacionadoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['item_id__descripcion']
    filterset_fields = ['activo', 'item_id', 'item_relacionado_id']


class tblitemcategoriaViewSet(ModelViewSet):
    queryset = tblitemcategoria.objects.filter(activo=True).order_by('pk')
    serializer_class = tblitemcategoriaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['iditem_id__descripcion']
    filterset_fields = ['activo', 'iditem_id']




class TbldetallepedidoViewSet(ModelViewSet):
    queryset = Tbldetallepedido.objects.filter(activo=True).order_by('pk')
    serializer_class = TbldetallepedidoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['idpedido__id', 'idproduct__descripcion']
    filterset_fields = ['activo', 'idpedido_id', 'idproduct_id', 'cantidad', 'preciototal', 'preciunitario']



class TransaccionViewSet(ModelViewSet):
    queryset = tblTransaccion.objects.filter(activo=True).order_by('pk')
    serializer_class = TransaccionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nombre_en_tarjeta']
    filterset_fields = [
    "metodo_pago",
    "nombre_en_tarjeta",
    "numero_tarjeta",
    "monto_total"
]

