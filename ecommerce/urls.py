from rest_framework.routers import SimpleRouter
from ecommerce import views
from django.conf import settings
from django.conf.urls.static import static

router = SimpleRouter()

urlpatterns = [
]
router.register(r'marca', views.MarcaViewSet)
router.register(r'tblitem', views.TblitemViewSet)
router.register(r'tblimagenitem', views.TblimagenitemViewSet)


router.register(r'tblitemclase', views.TblitemclaseViewSet)
router.register(r'tblitempropiedad', views.TblitempropiedadViewSet)
router.register(r'tblitemclasepropiedad', views.TblitemclasepropiedadViewSet)


router.register(r'tblitemrelacionado', views.TblitemrelacionadoViewSet)

router.register(r'tblusuario', views.TblusuarioViewSet)
router.register(r'valoracion', views.ValoracionViewSet)

urlpatterns = router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

