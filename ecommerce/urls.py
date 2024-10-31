from rest_framework.routers import SimpleRouter
from ecommerce import views
from django.conf import settings
from django.conf.urls.static import static

router = SimpleRouter()

urlpatterns = [
]


router.register(r'administracion', views.AdministracionViewSet)
router.register(r'cupon', views.CuponViewSet)
router.register(r'marca', views.MarcaViewSet)
router.register(r'moneda', views.MonedaViewSet)
router.register(r'promocion', views.PromocionViewSet)
router.register(r'tblcarrito', views.TblcarritoViewSet)
router.register(r'tblitem', views.TblitemViewSet)
router.register(r'tblnoticia', views.TblnoticiaViewSet)
router.register(r'tblpedido', views.TblpedidoViewSet)
router.register(r'tblslider', views.TblsliderViewSet)
router.register(r'tblusuario', views.TblusuarioViewSet)
router.register(r'tipocambio', views.TipocambioViewSet)
router.register(r'valoracion', views.ValoracionViewSet)
router.register(r'tbldetallecarrito', views.TbldetallecarritoViewSet)
router.register(r'tblimagenitem', views.TblimagenitemViewSet)
router.register(r'tblitemclase', views.TblitemclaseViewSet)
router.register(r'tblitemclasepropiedad', views.TblitemclasepropiedadViewSet)
router.register(r'tblitempropiedad', views.TblitempropiedadViewSet)
router.register(r'tblitemrelacionado', views.TblitemrelacionadoViewSet)
router.register(r'tbldetallepedido', views.TbldetallepedidoViewSet)

urlpatterns = router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

