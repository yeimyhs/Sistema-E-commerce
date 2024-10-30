from rest_framework.serializers import ModelSerializer
from ecommerce.models import Administracion, Cupon, Marca, Moneda, Promocion, Tblcarrito, Tblitem, Tblnoticia, Tblpedido, Tblslider, Tblusuario, Tipocambio, Valoracion, Tbldetallecarrito, Tblimagenitem, Tblitemclase, Tblitemclasepropiedad, Tblitempropiedad, Tblitemrelacionado, Tbldetallepedido


class AdministracionSerializer(ModelSerializer):

    class Meta:
        model = Administracion
        depth = 2
        fields = '__all__'


class CuponSerializer(ModelSerializer):

    class Meta:
        model = Cupon
        depth = 2
        fields = '__all__'


class MarcaSerializer(ModelSerializer):

    class Meta:
        model = Marca
        depth = 2
        fields = '__all__'


class MonedaSerializer(ModelSerializer):

    class Meta:
        model = Moneda
        depth = 2
        fields = '__all__'


class PromocionSerializer(ModelSerializer):

    class Meta:
        model = Promocion
        depth = 2
        fields = '__all__'


class TblcarritoSerializer(ModelSerializer):

    class Meta:
        model = Tblcarrito
        depth = 2
        fields = '__all__'


class TblitemSerializer(ModelSerializer):

    class Meta:
        model = Tblitem
        depth = 2
        fields = '__all__'


class TblnoticiaSerializer(ModelSerializer):

    class Meta:
        model = Tblnoticia
        depth = 2
        fields = '__all__'


class TblpedidoSerializer(ModelSerializer):

    class Meta:
        model = Tblpedido
        depth = 2
        fields = '__all__'


class TblsliderSerializer(ModelSerializer):

    class Meta:
        model = Tblslider
        depth = 2
        fields = '__all__'


class TblusuarioSerializer(ModelSerializer):

    class Meta:
        model = Tblusuario
        depth = 2
        fields = '__all__'


class TipocambioSerializer(ModelSerializer):

    class Meta:
        model = Tipocambio
        depth = 2
        fields = '__all__'


class ValoracionSerializer(ModelSerializer):

    class Meta:
        model = Valoracion
        depth = 2
        fields = '__all__'


class TbldetallecarritoSerializer(ModelSerializer):

    class Meta:
        model = Tbldetallecarrito
        depth = 2
        fields = '__all__'


class TblimagenitemSerializer(ModelSerializer):

    class Meta:
        model = Tblimagenitem
        depth = 2
        fields = '__all__'


class TblitemclaseSerializer(ModelSerializer):

    class Meta:
        model = Tblitemclase
        depth = 2
        fields = '__all__'


class TblitemclasepropiedadSerializer(ModelSerializer):

    class Meta:
        model = Tblitemclasepropiedad
        depth = 2
        fields = '__all__'


class TblitempropiedadSerializer(ModelSerializer):

    class Meta:
        model = Tblitempropiedad
        depth = 2
        fields = '__all__'


class TblitemrelacionadoSerializer(ModelSerializer):

    class Meta:
        model = Tblitemrelacionado
        depth = 2
        fields = '__all__'


class TbldetallepedidoSerializer(ModelSerializer):

    class Meta:
        model = Tbldetallepedido
        depth = 2
        fields = '__all__'
