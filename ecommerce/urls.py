from rest_framework.routers import SimpleRouter
from ecommerce import views
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path , re_path, reverse
from django.urls import path,include, re_path
from knox import views as knox_views

from django.conf import settings
from django.conf.urls.static import static
router = SimpleRouter()

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='knox_login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    path('register/', views.RegisterAPI.as_view(), name='register'),
    path('userinfo/', views.UserInfoView.as_view(), name='userinfo'),
    
    path('crearpagoizip/', views.create_payment, name='create_payment'),
    path('auth-credentials/', views.AuthCredentialsView.as_view(), name='auth-credentials'),
    
    path('clases_propiedades/', views.ClasesYPropiedadesView.as_view(), name='clases_propiedades'),
    path('filtrobusqueda/', views.BusquedaDinamicaViewSet.as_view({'get': 'list'})),
    
    path('bulkitem/', views.BulkUploadItemsAPIView.as_view()),
    
    #path('upload_xlsx/', views.upload_xlsx, name='upload_xlsx'),
    #path('download_template/', views.download_template, name='download_template'),
]
router.register(r'administracion', views.AdministracionViewSet)
router.register(r'cupon', views.CuponViewSet)
router.register(r'marca', views.MarcaViewSet)
router.register(r'sede', views.TblsedeViewSet)
router.register(r'tblreclamacion', views.TblreclamacionViewSet)
router.register(r'tblcategoria', views.TblcategoriaViewSet)
router.register(r'tblflete', views.FleteViewSet)
router.register(r'tblmodelo', views.TblmodeloViewSet)
router.register(r'moneda', views.MonedaViewSet)
router.register(r'promocion', views.PromocionViewSet)
router.register(r'tblcarrito', views.TblcarritoViewSet)
router.register(r'tblitem', views.TblitemViewSet)
router.register(r'tblnoticia', views.TblnoticiaViewSet)
router.register(r'tblpedido', views.TblpedidoViewSet)
router.register(r'TblCarrusel', views.TblCarruselViewSet)
router.register(r'tblusuario', views.TblusuarioViewSet)
router.register(r'tipocambio', views.TipocambioViewSet)
router.register(r'valoracion', views.ValoracionViewSet)
router.register(r'tbldetallecarrito', views.TbldetallecarritoViewSet)
router.register(r'tblimagenitem', views.TblimagenitemViewSet)
router.register(r'tblitemclase', views.TblitemclaseViewSet)
router.register(r'tblitemclasevinculo', views.tblitemclasevinculoViewSet)
#router.register(r'tblitempropiedad', views.TblitempropiedadViewSet)

router.register(r'tblitemcategoria', views.tblitemcategoriaViewSet)
router.register(r'tblitemrelacionado', views.TblitemrelacionadoViewSet)
router.register(r'tbldetallepedido', views.TbldetallepedidoViewSet)
router.register(r'tblitemcupon', views.tblitemcuponSerializerViewSet)

urlpatterns = urlpatterns + router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

