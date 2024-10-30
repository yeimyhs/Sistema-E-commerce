from rest_framework.viewsets import ModelViewSet
from ecommerce.serializers import AdministracionSerializer, CuponSerializer, MarcaSerializer, MonedaSerializer, PromocionSerializer, TblcarritoSerializer, TblitemSerializer, TblnoticiaSerializer, TblpedidoSerializer, TblsliderSerializer, TblusuarioSerializer, TipocambioSerializer, ValoracionSerializer, TbldetallecarritoSerializer, TblimagenitemSerializer, TblitemclaseSerializer, TblitemclasepropiedadSerializer, TblitempropiedadSerializer, TblitemrelacionadoSerializer, TbldetallepedidoSerializer
from ecommerce.models import Administracion, Cupon, Marca, Moneda, Promocion, Tblcarrito, Tblitem, Tblnoticia, Tblpedido, Tblslider, Tblusuario, Tipocambio, Valoracion, Tbldetallecarrito, Tblimagenitem, Tblitemclase, Tblitemclasepropiedad, Tblitempropiedad, Tblitemrelacionado, Tbldetallepedido


class AdministracionViewSet(ModelViewSet):
    queryset = Administracion.objects.order_by('pk')
    serializer_class = AdministracionSerializer


class CuponViewSet(ModelViewSet):
    queryset = Cupon.objects.order_by('pk')
    serializer_class = CuponSerializer


class MarcaViewSet(ModelViewSet):
    queryset = Marca.objects.order_by('pk')
    serializer_class = MarcaSerializer


class MonedaViewSet(ModelViewSet):
    queryset = Moneda.objects.order_by('pk')
    serializer_class = MonedaSerializer


class PromocionViewSet(ModelViewSet):
    queryset = Promocion.objects.order_by('pk')
    serializer_class = PromocionSerializer


class TblcarritoViewSet(ModelViewSet):
    queryset = Tblcarrito.objects.order_by('pk')
    serializer_class = TblcarritoSerializer


class TblitemViewSet(ModelViewSet):
    queryset = Tblitem.objects.order_by('pk')
    serializer_class = TblitemSerializer


class TblnoticiaViewSet(ModelViewSet):
    queryset = Tblnoticia.objects.order_by('pk')
    serializer_class = TblnoticiaSerializer


class TblpedidoViewSet(ModelViewSet):
    queryset = Tblpedido.objects.order_by('pk')
    serializer_class = TblpedidoSerializer


class TblsliderViewSet(ModelViewSet):
    queryset = Tblslider.objects.order_by('pk')
    serializer_class = TblsliderSerializer


class TblusuarioViewSet(ModelViewSet):
    queryset = Tblusuario.objects.order_by('pk')
    serializer_class = TblusuarioSerializer


class TipocambioViewSet(ModelViewSet):
    queryset = Tipocambio.objects.order_by('pk')
    serializer_class = TipocambioSerializer


class ValoracionViewSet(ModelViewSet):
    queryset = Valoracion.objects.order_by('pk')
    serializer_class = ValoracionSerializer


class TbldetallecarritoViewSet(ModelViewSet):
    queryset = Tbldetallecarrito.objects.order_by('pk')
    serializer_class = TbldetallecarritoSerializer


class TblimagenitemViewSet(ModelViewSet):
    queryset = Tblimagenitem.objects.order_by('pk')
    serializer_class = TblimagenitemSerializer


class TblitemclaseViewSet(ModelViewSet):
    queryset = Tblitemclase.objects.order_by('pk')
    serializer_class = TblitemclaseSerializer


class TblitemclasepropiedadViewSet(ModelViewSet):
    queryset = Tblitemclasepropiedad.objects.order_by('pk')
    serializer_class = TblitemclasepropiedadSerializer


class TblitempropiedadViewSet(ModelViewSet):
    queryset = Tblitempropiedad.objects.order_by('pk')
    serializer_class = TblitempropiedadSerializer


class TblitemrelacionadoViewSet(ModelViewSet):
    queryset = Tblitemrelacionado.objects.order_by('pk')
    serializer_class = TblitemrelacionadoSerializer


class TbldetallepedidoViewSet(ModelViewSet):
    queryset = Tbldetallepedido.objects.order_by('pk')
    serializer_class = TbldetallepedidoSerializer
