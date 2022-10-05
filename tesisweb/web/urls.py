from django.urls import path, include, re_path
from . import views

urlpatterns = [

    
    path('solicitud/', views.peticion_apertura),


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