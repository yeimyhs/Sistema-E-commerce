from rest_framework.serializers import ModelSerializer
from ecommerce.models import Administracion, Cupon, Marca, Moneda, Promocion, Tblcarrito, Tblitem, Tblnoticia, Tblpedido, Tblslider, Tblusuario, Tipocambio, Valoracion, Tbldetallecarrito, Tblimagenitem, Tblitemclase, Tblitemclasepropiedad, Tblitempropiedad, Tblitemrelacionado, Tbldetallepedido


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


class TblitemSerializer(ModelSerializer):

    class Meta:
        model = Tblitem
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


class TblusuarioSerializer(ModelSerializer):

    class Meta:
        model = Tblusuario
        fields = '__all__'


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


class TblitemclaseSerializer(ModelSerializer):

    class Meta:
        model = Tblitemclase
        fields = '__all__'


class TblitemclasepropiedadSerializer(ModelSerializer):

    class Meta:
        model = Tblitemclasepropiedad
        fields = '__all__'


class TblitempropiedadSerializer(ModelSerializer):

    class Meta:
        model = Tblitempropiedad
        fields = '__all__'


class TblitemrelacionadoSerializer(ModelSerializer):

    class Meta:
        model = Tblitemrelacionado
        fields = '__all__'


class TbldetallepedidoSerializer(ModelSerializer):

    class Meta:
        model = Tbldetallepedido
        fields = '__all__'
