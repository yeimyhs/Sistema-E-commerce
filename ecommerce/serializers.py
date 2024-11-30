from rest_framework.serializers import ModelSerializer
from ecommerce.models import Administracion, Cupon, Marca, Moneda, Promocion, Tblcarrito, Tblitem, Tblnoticia, Tblpedido, Tblslider, Tipocambio, Valoracion, Tbldetallecarrito, Tblimagenitem, Tblitemclase, Tblitemclasepropiedad, Tblitempropiedad, Tblitemrelacionado, Tbldetallepedido

from .models import *
from .serializers import *

from rest_framework import serializers

from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from django.contrib.auth import authenticate

class CustomAuthTokenSerializer(serializers.Serializer):
    nombreusuario = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        # Usar el campo 'nombreusuario' en lugar de 'username'
        user = authenticate(nombreusuario=attrs['nombreusuario'], password=attrs['password'])
        if user is None:
            raise serializers.ValidationError("Credenciales inválidas")
        attrs['user'] = user
        return attrs


class AdministracionSerializer(ModelSerializer):

    class Meta:
        model = Administracion
        fields = '__all__'


class CuponSerializer(ModelSerializer):

    class Meta:
        model = Cupon
        fields = '__all__'


class MarcaSerializer(ModelSerializer):

    class Meta:
        model = Marca
        fields = '__all__'


class MonedaSerializer(ModelSerializer):

    class Meta:
        model = Moneda
        fields = '__all__'


class PromocionSerializer(ModelSerializer):

    class Meta:
        model = Promocion
        fields = '__all__'


class TblcarritoSerializer(ModelSerializer):

    class Meta:
        model = Tblcarrito
        fields = '__all__'




class TblnoticiaSerializer(ModelSerializer):

    class Meta:
        model = Tblnoticia
        fields = '__all__'


class TblpedidoSerializer(ModelSerializer):

    class Meta:
        model = Tblpedido
        fields = '__all__'


class TblsliderSerializer(ModelSerializer):

    class Meta:
        model = Tblslider
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
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
        model = Tipocambio
        fields = '__all__'


class ValoracionSerializer(ModelSerializer):

    class Meta:
        model = Valoracion
        fields = '__all__'


class TbldetallecarritoSerializer(ModelSerializer):

    class Meta:
        model = Tbldetallecarrito
        fields = '__all__'


class TblimagenitemSerializer(ModelSerializer):

    class Meta:
        model = Tblimagenitem
        fields = '__all__'


class TblitempropiedadSerializer(ModelSerializer):

    class Meta:
        model = Tblitempropiedad
        fields = '__all__'


class TblitemclaseSerializer(ModelSerializer):
    class Meta:
        model = Tblitemclase
        fields = '__all__'
        
class PropiedadesxClasesSerializer(ModelSerializer):
    propiedades = serializers.SerializerMethodField()
    class Meta:
        model = Tblitemclase
        fields = '__all__'
        
    def get_propiedades(self, obj):
        propiedades = Tblitempropiedad.objects.filter(idclase=obj)
        return TblitempropiedadSerializer(propiedades, many=True).data

class TblitemclasepropiedadSerializer(ModelSerializer):
    clase = TblitemclaseSerializer(source='idclase', read_only=True)
    propiedad = TblitempropiedadSerializer(source='idpropiedad', read_only=True)

    class Meta:
        model = Tblitemclasepropiedad
        fields = '__all__'




class TblitemrelacionadoSerializer(ModelSerializer):

    class Meta:
        model = Tblitemrelacionado
        fields = '__all__'


class TbldetallepedidoSerializer(ModelSerializer):

    class Meta:
        model = Tbldetallepedido
        fields = '__all__'

class NombresTblitemClasePropiedadSerializer(serializers.ModelSerializer):
    clase_nombre = serializers.CharField(source='idclase.nombre', read_only=True)
    propiedad_nombre = serializers.CharField(source='idpropiedad.nombre', read_only=True)

    class Meta:
        model = Tblitemclasepropiedad
        fields = ['clase_nombre', 'propiedad_nombre'] 
        
class TblitemSerializer(ModelSerializer):
    clases_propiedades = serializers.SerializerMethodField()
    #imagen_marca =  MarcaSerializer(source='idmarca', read_only=True)
    imagenes_producto =  serializers.SerializerMethodField()
    class Meta:
        model = Tblitem
        fields = ['idproduct', 'codigosku', 'stock', 'descripcion', 'destacado', 'agotado', 
                  'nuevoproducto', 'preciorebajado', 'precionormal', 'imagenprincipal',
                  
                  'estado','fechacreacion', 'fechamodificacion', 'clases_propiedades', 'imagenes_producto']
    def get_clases_propiedades(self, obj):
        clases_propiedades = Tblitemclasepropiedad.objects.filter(idproduct=obj)
        return NombresTblitemClasePropiedadSerializer(clases_propiedades, many=True).data

        
    def get_imagenes_producto(self, obj):
        imagenes_producto = Tblimagenitem.objects.filter(idproduct=obj)
        return TblimagenitemSerializer(imagenes_producto, many=True).data   