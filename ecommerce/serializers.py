from rest_framework.serializers import ModelSerializer
from ecommerce.models import Administracion, Cupon, Marca, Moneda, Promocion, Tblcarrito, Tblitem, Tblnoticia, Tblpedido, TblCarrusel, Tipocambio, Valoracion, Tbldetallecarrito, Tblimagenitem, Tblitemclase, Tblitempropiedad, Tblitemrelacionado, Tbldetallepedido

from .models import *
from .serializers import *

from rest_framework import serializers

from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser

from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser

class CustomAuthTokenSerializer(serializers.Serializer):
    nombreusuario = serializers.CharField(label="Nombre de usuario")
    password = serializers.CharField(label="Contraseña", style={"input_type": "password"})

    def validate(self, attrs):
        nombreusuario = attrs.get("nombreusuario")
        password = attrs.get("password")

        # Validar si faltan campos
        if not nombreusuario and not password:
            raise serializers.ValidationError(
                {
                    "error": {
                        "code": "missing_fields",
                        "message": "El nombre de usuario y la contraseña son obligatorios."
                    }
                },
                code="authorization",
            )
        elif not nombreusuario:
            raise serializers.ValidationError(
                {
                    "error": {
                        "code": "missing_username",
                        "message": "El nombre de usuario es obligatorio."
                    }
                },
                code="authorization",
            )
        elif not password:
            raise serializers.ValidationError(
                {
                    "error": {
                        "code": "missing_password",
                        "message": "La contraseña es obligatoria."
                    }
                },
                code="authorization",
            )

        # Autenticar al usuario
        user = authenticate(nombreusuario=nombreusuario, password=password)

        # Validar credenciales inválidas
        if not user:
            raise serializers.ValidationError(
                {
                    "error": {
                        "code": "invalid_credentials",
                        "message": "Las credenciales proporcionadas no son válidas. Por favor, intente de nuevo."
                    }
                },
                code="authorization",
            )

        # Verificar si la cuenta está deshabilitada
        if not user.estado:
            raise serializers.ValidationError(
                {
                    "error": {
                        "code": "account_disabled",
                        "message": "Esta cuenta está deshabilitada. Contacte con el administrador."
                    }
                },
                code="authorization",
            )

        # Validar si el usuario está inactivo
        if not user.is_active:
            raise serializers.ValidationError(
                {
                    "error": {
                        "code": "account_inactive",
                        "message": "Esta cuenta está inactiva. Por favor, contacte con el administrador."
                    }
                },
                code="authorization",
            )

        # Si todo es válido, se retorna el usuario
        attrs["user"] = user
        return attrs
    


class TblitemBasicoSerializer(ModelSerializer):

    class Meta:
        #depth = 1
        model = Tblitem
        fields = '__all__'
        
class AdministracionSerializer(ModelSerializer):

    class Meta:
        #depth = 1
        model = Administracion
        fields = '__all__'


class CuponSerializer(ModelSerializer):

    class Meta:
        #depth = 1
        model = Cupon
        fields = '__all__'


class MarcaSerializer(ModelSerializer):

    class Meta:
        #depth = 1
        model = Marca
        fields = '__all__'

class TblcategoriaSerializer(ModelSerializer):

    class Meta:
        #depth = 1
        model = Tblcategoria
        fields = '__all__'
        
class FleteSerializer(ModelSerializer):

    class Meta:
        #depth = 1
        model = Flete
        fields = '__all__'
        

class FleteCategoriaValorSerializer(serializers.Serializer):
    idcategoria = serializers.IntegerField()
    val = serializers.DecimalField(max_digits=20, decimal_places=2)

class DepartamentoSerializer(serializers.Serializer):
    iddepartamento = serializers.CharField(max_length=2)
    valores = FleteCategoriaValorSerializer(many=True)

    def create(self, validated_data):
        iddepartamento = validated_data['iddepartamento']
        valores = validated_data['valores']

        # Crear una lista de instancias Flete
        fletes = [
            Flete(
                iddepartamento=iddepartamento,
                idcategoria_id=valor['idcategoria'],
                precio=valor['val']
            )
            for valor in valores
        ]

        # Inserción masiva
        Flete.objects.bulk_create(fletes)
        return validated_data


class tblitemcategoriaSerializer(ModelSerializer):
    categoria_detalle =TblcategoriaSerializer(source='idcategoria', read_only=True)
    class Meta:
        #depth = 1
        model = tblitemcategoria
        fields = '__all__'

class MonedaSerializer(ModelSerializer):

    class Meta:
        #depth = 1
        model = Moneda
        fields = '__all__'


class PromocionSerializer(ModelSerializer):

    class Meta:
        #depth = 1
        model = Promocion
        fields = '__all__'


class TblcarritoSerializer(ModelSerializer):

    class Meta:
        #depth = 1
        model = Tblcarrito
        fields = '__all__'




class TblnoticiaSerializer(ModelSerializer):

    class Meta:
        #depth = 1
        model = Tblnoticia
        fields = '__all__'





class TblCarruselSerializer(ModelSerializer):

    class Meta:
        #depth = 1
        model = TblCarrusel
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        #depth = 1
        model = CustomUser
        fields = ['activo',
            'id',
            'email',
            'nombre',
            'apellidos',
            'nombreusuario',  # Añadir el campo de nombreusuario como USERNAME_FIELD
            'direccion',
            'departamento','provincia','distrito',
            'estado',
            'fechacreacion',  # Campo de creación automática
            'fechamodificacion',  # Campo de modificación automática
            'telefono',
            'imagenperfil',
            
            'email_verified_at',
            'remember_token',
            'is_staff',
        ]

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        #depth = 1
        model = CustomUser
        fields = [
            'email', 'password', 'nombre', 'apellidos', 
            'nombreusuario','telefono','imagenperfil',
            'direccion','departamento','provincia','distrito', 'estado', 'is_staff',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            nombre=validated_data.get('nombre'),
            apellidos=validated_data.get('apellidos'),
            nombreusuario=validated_data['nombreusuario'],  # Ahora es el campo de USERNAME_FIELD
            direccion=validated_data.get('direccion'),
            departamento=validated_data.get('departamento'),
            provincia=validated_data.get('provincia'),
            distrito=validated_data.get('distrito'),
            telefono=validated_data.get('telefono'),
            imagenperfil=validated_data.get('imagenperfil'), 
            
            estado=validated_data.get('estado'),
            is_staff=validated_data.get('is_staff')
        )
        return user

class TipocambioSerializer(ModelSerializer):

    class Meta:
        #depth = 1
        model = Tipocambio
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['moneda_detalle'] = MonedaSerializer(source='idmoneda', read_only=True)



class ValoracionSerializer(ModelSerializer):
    user_detalle = CustomUserSerializer(source='iduser', read_only=True)
    class Meta:
        #depth = 1
        model = Valoracion
        fields = '__all__'


class TbldetallecarritoSerializer(ModelSerializer):

    class Meta:
        #depth = 1
        model = Tbldetallecarrito
        fields = '__all__'


class TblimagenitemSerializer(ModelSerializer):

    class Meta:
        #depth = 1
        model = Tblimagenitem
        fields = '__all__'

class MultipleImagenItemSerializer(serializers.Serializer):
    idproduct = serializers.IntegerField()  # ID del producto relacionado
    imagenes = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True
    )

    def create(self, validated_data):
        idproduct = validated_data.get('idproduct')
        imagenes = validated_data.get('imagenes')
        items = [
            Tblimagenitem(idproduct_id=idproduct, imagen=imagen, estado=1)  # Cambia estado según tu lógica
            for imagen in imagenes
        ]
        return Tblimagenitem.objects.bulk_create(items)  # Crea todas las imágenes de golpe


class TblitempropiedadSerializer(ModelSerializer):

    class Meta:
        #depth = 1
        model = Tblitempropiedad
        fields = '__all__'


class TblitemclaseSerializer(ModelSerializer):
    class Meta:
        #depth = 1
        model = Tblitemclase
        fields = '__all__'
        
class PropiedadesxClasesSerializer(ModelSerializer):
    propiedades = serializers.SerializerMethodField()
    class Meta:
        #depth = 1
        model = Tblitemclase
        fields = '__all__'
        
    def get_propiedades(self, obj):
        propiedades = Tblitempropiedad.objects.filter(idclase=obj)
        return TblitempropiedadSerializer(propiedades, many=True).data

class TblitemclasevinculoSerializer(ModelSerializer):
    clase = TblitemclaseSerializer(source='idclase', read_only=True)

    class Meta:
        #depth = 1
        model = tblitemclasevinculo
        fields = '__all__'

class tblitemcuponSerializer(ModelSerializer):
    class Meta:
        #depth = 1
        model = tblitemcupon
        fields = '__all__'




class TblitemrelacionadoSerializer(ModelSerializer):
    item_relacionado_detalle = TblitemBasicoSerializer(source='item_relacionado', read_only=True)

    class Meta:
        #depth = 1
        model = Tblitemrelacionado
        fields = '__all__'  
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item_detalle'] = TblitemBasicoSerializer(source='item', read_only=True)



    
        
class TblreclaisionSerializer(ModelSerializer):

    class Meta:
        #depth = 1
        model = Tblreclamacion
        fields = '__all__'
        
class TblsedeSerializer(ModelSerializer):

    class Meta:
        #depth = 1
        model = Tblsede
        fields = '__all__'

class TblmodeloSerializer(ModelSerializer):
    marca_detalle = MarcaSerializer(source='idmarca', read_only=True)
    class Meta:
        #depth = 1
        model = Tblmodelo
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['marca_detalle'] = MarcaSerializer(source='idmarca', read_only=True)


class NombrestblitemClaseVinculoSerializer(serializers.ModelSerializer):
    clase_nombre = serializers.CharField(source='idclase.nombre', read_only=True)
    idclase = serializers.IntegerField(source='idclase.pk', read_only=True)

    class Meta:
        #depth = 1
        model = tblitemclasevinculo
        fields = ['id','activo','idclase','clase_nombre', 'propiedad'] 
        
class TblitemSerializer(ModelSerializer):
    clases_propiedades = serializers.SerializerMethodField()
    categorias = serializers.SerializerMethodField()
    imagenes_producto = serializers.SerializerMethodField()
    cupones = serializers.SerializerMethodField()
    items_relacionados = serializers.SerializerMethodField()

    class Meta:
        #depth = 1
        model = Tblitem
        fields = '__all__'  # Inicialmente incluye todos los campos del modelo.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar dinámicamente el campo marca_detalle
        self.fields['modelo_detalle'] = TblmodeloSerializer(source='idmodelo', read_only=True)

    def get_clases_propiedades(self, obj):
        clases_propiedades = tblitemclasevinculo.objects.filter(iditem=obj)
        return NombrestblitemClaseVinculoSerializer(clases_propiedades, many=True).data

    def get_imagenes_producto(self, obj):
        imagenes_producto = Tblimagenitem.objects.filter(idproduct=obj)
        return TblimagenitemSerializer(imagenes_producto, many=True).data

    def get_cupones(self, obj):
        # Muestra cupones solo si se han prefetch en la consulta (control en la vista)
        return tblitemcuponSerializer(obj.cupon_relacionado.all(), many=True).data
    
    def get_categorias(self, obj):
        # Muestra cupones solo si se han prefetch en la consulta (control en la vista)
        return tblitemcategoriaSerializer(obj.categoria_relacionada.all(), many=True).data

    def get_items_relacionados(self, obj):
        items_relacionados = Tblitemrelacionado.objects.filter(item=obj, activo=True)
        return TblitemrelacionadoSerializer(items_relacionados, many=True).data
    




from rest_framework import serializers



from rest_framework import serializers

class TblitemTestSerializer(serializers.Serializer):
    item = serializers.JSONField()
    vinculos = serializers.CharField(required=False, allow_blank=True)
    categorias = serializers.CharField(required=False, allow_blank=True)
    cupones = serializers.CharField(required=False, allow_blank=True)
    itemsrelacionados = serializers.CharField(required=False, allow_blank=True)
    imagenes_eliminartodas = serializers.BooleanField(required=False, default=False)
    imagenes = serializers.ListField(
        child=serializers.ImageField(),
        required=False
    )
    imagenprincipal = serializers.ImageField(required=False)
    idmodelo = serializers.IntegerField(required=False)
    
    
    
class PedidoConDetallesSerializer(serializers.ModelSerializer):
    detalleitems = serializers.SerializerMethodField()

    class Meta:
        model = Tblpedido
        fields = ['idpedido', 'idcliente', 'subtotal', 'direcciondestino', 'total', 'igv', 'totaldescuento', 'idcupon', 'idmoneda', 'estado', 'detalles']
    def get_detalleitems(self, obj):
        detalleitems = Tbldetallepedido.objects.filter(idpedido=obj)
        return TbldetallepedidoSerializer(detalleitems, many=True).data

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        pedido = Tblpedido.objects.create(**validated_data)
        for detalle_data in detalles_data:
            Tbldetallepedido.objects.create(idpedido=pedido, **detalle_data)
        return pedido
    
    
class TbldetallepedidoSerializer(ModelSerializer):
    item_detalle = TblitemSerializer(source='idproduct', read_only=True)
    class Meta:
        #depth = 1
        model = Tbldetallepedido
        fields = '__all__'

class TransaccionSerializer(ModelSerializer):
    class Meta:
        #depth = 1
        model = tblTransaccion
        fields = '__all__'     
        
class TblpedidoSerializer(ModelSerializer):
    detalleitems = serializers.SerializerMethodField()
    moneda_detalle =MonedaSerializer(source='idmoneda', read_only=True)
    cupon_detalle = CuponSerializer(source='idcupon', read_only=True)
    sede_detalle = TblsedeSerializer(source='idsede', read_only=True)
    transaccion_detalle = TransaccionSerializer(source='idtransaccion', read_only=True)
    
    class Meta:
        #depth = 1
        model = Tblpedido
        fields = '__all__'
    
    def get_detalleitems(self, obj):
        detalleitems = Tbldetallepedido.objects.filter(idpedido=obj)
        return TbldetallepedidoSerializer(detalleitems, many=True).data


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("No se encontró un usuario con ese correo.")
        return value