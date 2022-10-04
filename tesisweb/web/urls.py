from django.urls import path, include, re_path
from . import views
from .views import agregarfoto, SessionView, WhoAmIView#, login_view, registrarusuario, 
#from .views import ContratosList
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView
#from rest_framework_simplejwt import views as jwt_views

# router = routers.DefaultRouter()
# router.register(r'contratos', views.ContratosList)

router = routers.DefaultRouter()
router.register(r'subirfotos', views.agregarfoto)
#router.register(r'registro', views.registrarusuario)

urlpatterns = [
    # path('', views.index, name='index'),
    # path('interacciones', views.interaccionesss, name='interacciones'),
    # path('editarcontrato/<str:contrato_id>/', views.editarcontrato, name='editarcontrato'),
    # path('eliminarusuario/<int:cedula_id>/', views.eliminarusuario, name='eliminarusuario'),
    # path('eliminarhorario/<int:id_web>', views.eliminarhorario, name='eliminarhorario'),
    # path('editarusuario/<int:cedula_id>', views.editarusuario, name='editarusuario'),
    # path('agregarcontrato', views.agregarcontrato, name='agregarcontrato'),
    # path('eliminarcontrato/<str:contrato_id>/', views.eliminarcontrato, name='eliminarcontrato'),
    # path('editarcontrato', views.seleccionarcontrato, name='seleccionarcontrato'),
    # path('eliminarfoto/<int:cedula_id>/', views.eliminarfoto, name='eliminarfoto'),
    path('api', include(router.urls)),
    #re_path(r'^contratos/$', views.seleccionarcontratoapi),
    #re_path(r'^editarcontratoapi/(?P<contrato_id>\w+)$', views.editarcontratoapi),
    re_path(r'^agregarcontratosapi/$', views.agregarcontratosapi),
    #re_path(r'^removercontratosapi/(?P<contrato_id>[\w\s]+)/$', views.eliminarcontratos),
    #re_path(r'^removercontratosapi/(?P<contrato_id>.*)/$', views.eliminarcontratos),
    re_path(r'^removercontratosapi/(?P<contrato_id>[\w\ ]+)/$', views.eliminarcontratos),
    re_path(r'^seleccionarcontratoapi/(?P<contrato_id>[\w\ ]+)/$', views.seleccionarcontratoapi),
    re_path(r'^dispositivosapi/(?P<contrato_id>[\w\ ]+)/$', views.dispositivosapi),
    re_path(r'^servidorlocalapi/(?P<contrato_id>[\w\ ]+)/$', views.servidorlocal),
    re_path(r'^probarservidorlocalapi/(?P<contrato_id>[\w\ ]+)/$', views.probar_conexion_servidorlocal),
    re_path(r'^editcontrato/agregarusuario/$', views.agregarusuarioapi),
    re_path(r'^editcontrato/eliminarusuario/(?P<cedula_id>[\w\ ]+)/$', views.eliminarusuarioapi),
    re_path(r'^editcontrato/buscarusuario/(?P<cedula_id>[\w\ ]+)/$', views.buscarusuarioapi),
    re_path(r'^editusuario/horarios/(?P<cedula_id>[\w\ ]+)/$', views.editarhorariosapi),
    re_path(r'^editusuario/foto/(?P<cedula_id>[\w\ ]+)/$', views.editarfotosapi),
    re_path(r'^editusuario/agregarid/$', views.agregartelegramidapi),
    re_path(r'^actividad/$', views.interaccionesapi),
    re_path(r'^apertura/$', views.aperturaa),
    re_path(r'^loginapi/$', views.loginapi, name='api-login'),
    path('logout/', views.logoutapi, name='api-logout'),
    path('csrf/', views.get_csrf, name='api-csrf'),
    path('session/', SessionView.as_view(), name='api-session'),
    path('apiregistro/', views.registraruser),
    re_path(r'^(?P<path>.*)/$', views.index),

    #path('si/', jwt_views.TokenObtainPairView.as_view()),
    #path('ka/', jwt_views.TokenRefreshView.as_view()),
    #path('protegida/', Protegida.as_view()),
    #path('registro/', registrarusuario.as_view()),
    #path('loginn/', Loogin.as_view()),
    
    #re_path(r'^loginapi/$', login_view.as_view()),
    path('whoami/', WhoAmIView.as_view(), name='api-whoami'),


]   

## En estos links esta la informacion que estoy usando para la
## autenticacion
# https://testdriven.io/blog/django-spa-auth/
# https://github.com/duplxey/django-spa-cookie-auth/tree/master/django_react_drf_same_origin/backend/api

## para las cookies
#https://peaku.co/es/preguntas/3521-la-cookie-no-se-configura-en-el-cliente-angular

# https://stackoverflow.com/questions/40851475/pass-django-csrf-token-to-angular-with-csrf-cookie-httponly/72850520#72850520
# https://stackoverflow.com/questions/58266828/how-to-add-csrf-token-to-angular-8-post-request-from-django-2-2
# https://stackoverflow.com/questions/43364213/ng2-get-csrf-token-from-cookie-post-it-as-header/43365939#43365939