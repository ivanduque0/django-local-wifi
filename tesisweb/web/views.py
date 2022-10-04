from django.http.response import JsonResponse
from .models import horariospermitidos, interacciones, usuarios, apertura, User
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .serializers import aperturaserializer
import pytz
import os
import urllib.request
from datetime import datetime

dias_semana = ("Lunes","Martes","Miercoles","Jueves","Viernes","Sabado","Domingo")
ultimahora = datetime.strptime('23:59:59', '%H:%M:%S').time()
primerahora = datetime.strptime('00:00:00', '%H:%M:%S').time()
razon1=os.environ.get("RAZON_ACCESO1")
razon2=os.environ.get("RAZON_ACCESO2")
razon3=os.environ.get("RAZON_ACCESO3")
razon4=os.environ.get("RAZON_ACCESO4")
acceso1=os.environ.get('URL_ACCESO1')
acceso2=os.environ.get('URL_ACCESO2')
acceso3=os.environ.get('URL_ACCESO3')
acceso4=os.environ.get('URL_ACCESO4')
CONTRATO=os.environ.get("CONTRATO")

accesodict = {'1':acceso1, '2':acceso2, '3':acceso3, '4':acceso4}


def aperturaconcedida(nombref, fechaf, horaf, razonf, contratof, cedulaf, acceso):
    
    try:
        urllib.request.urlopen(f'{accesodict[acceso]}/on')
    except:
        interacciones.objects.create(nombre=nombref, fecha=fechaf, hora=horaf, razon=razonf, contrato=f'fallo_{razonf}', cedula=cedulaf)
    finally:
        interacciones.objects.create(nombre=nombref, fecha=fechaf, hora=horaf, razon=razonf, contrato=contratof, cedula=cedulaf)
        	     

def aperturadenegada(acceso):

    try:
        urllib.request.urlopen(f'{accesodict[acceso]}/off')
    except:
        print("fallo en peticion http")
    finally:
        pass

@csrf_exempt
@api_view(['GET', 'POST'])
def aperturaa(request):

    if request.method == 'GET': 
        aperturainfo = apertura.objects.all()
        apertura_serializer = aperturaserializer(aperturainfo, many=True)
        return JsonResponse(apertura_serializer.data, safe=False)

    elif request.method == 'POST':
        aperturapost_serializer = aperturaserializer(data=request.data)
        if aperturapost_serializer.is_valid():
            accesoo= aperturapost_serializer.initial_data.get('acceso', None)
            id_usuarioo= aperturapost_serializer.initial_data.get('id_usuario', None)
            usuario=usuarios.objects.filter(id_usuario=id_usuarioo)
            if usuario:
                usuario=usuario[0]
                diasusuario = []
                etapadia=0
                etapadiaapertura=0
                cantidaddias = 0
                contadoraux = 0
                acceso_solicitud=accesoo
                cedula=usuario.cedula
                nombre=usuario.nombre
                horarios_permitidos=horariospermitidos.objects.filter(cedula=cedula)
                if horarios_permitidos != []:
                    tz = pytz.timezone('America/Caracas')
                    caracas_now = datetime.now(tz)
                    dia = caracas_now.weekday()
                    diahoy = dias_semana[dia]
                    for horario_permitido in horarios_permitidos:
                        diasusuario.append(horario_permitido.dia)
                    cantidaddias = diasusuario.count(dia)
                    for entrada, salida, _, dia in horarios_permitidos:
                        if 'Siempre' in diasusuario:
                            hora=str(caracas_now)[11:19]
                            horahoy = datetime.strptime(hora, '%H:%M:%S').time()
                            fecha=str(caracas_now)[:10]
                            etapadia=1
                            aperturaconcedida(nombre, fecha, horahoy, razon1, CONTRATO, cedula, accesoo)
                            etapadiaapertura=1
                        elif dia==diahoy and cantidaddias==1:
                            hora=str(caracas_now)[11:19]
                            horahoy = datetime.strptime(hora, '%H:%M:%S').time()
                            fecha=str(caracas_now)[:10]
                            etapadia=1
                            if entrada<salida:
                                if horahoy >= entrada and horahoy <= salida:
                                    #print('entrada concedida')
                                    aperturaconcedida(nombre, fecha, horahoy, razon1, CONTRATO, cedula, acceso_solicitud)
                                    etapadiaapertura=1
                                else:
                                    aperturadenegada(acceso_solicitud)
                                    #print('fuera de horario')
                            if entrada>salida:
                                if (horahoy>=entrada and horahoy <=ultimahora) or (horahoy>=primerahora and horahoy <= salida):
                                    #print('entrada concedida')
                                    aperturaconcedida(nombre, fecha, horahoy, razon1, CONTRATO, cedula, acceso_solicitud)
                                    etapadiaapertura=1
                                else:
                                    aperturadenegada(acceso_solicitud)
                                    #print('fuera de horario')
                        elif dia==diahoy and cantidaddias>1:
                            hora=str(caracas_now)[11:19]
                            horahoy = datetime.strptime(hora, '%H:%M:%S').time()
                            fecha=str(caracas_now)[:10]
                            etapadia=1
                            if entrada<salida:
                                if horahoy >= entrada and horahoy <= salida:
                                    #print('entrada concedida')
                                    aperturaconcedida(nombre, fecha, horahoy, razon1, CONTRATO, cedula, acceso_solicitud)
                                    etapadiaapertura=1
                                    contadoraux=0
                                else:
                                    contadoraux = contadoraux+1
                                    if contadoraux == cantidaddias:
                                        aperturadenegada(acceso_solicitud)
                                        contadoraux=0
                            if entrada>salida:
                                if (horahoy>=entrada and horahoy <=ultimahora) or (horahoy>=primerahora and horahoy <= salida):
                                    #print('entrada concedida')
                                    aperturaconcedida(nombre, fecha, horahoy, razon1, CONTRATO, cedula, acceso_solicitud)
                                    etapadiaapertura=1
                                    contadoraux=0
                                else:
                                    contadoraux = contadoraux+1
                                    if contadoraux == cantidaddias:
                                        aperturadenegada(acceso_solicitud)
                                        contadoraux=0
                                    #print('fuera de horario')
                    if etapadia==0 and etapadiaapertura==0:
                        aperturadenegada(acceso_solicitud)
                        #print('Dia no permitido')
                if horarios_permitidos == []:
                    aperturadenegada(acceso_solicitud) 
                    #print('este usuario no tiene horarios establecidos')
                diasusuario=[]
            else:
                aperturadenegada(acceso_solicitud) 
            return JsonResponse({'detail: solicitud hecha!'}, status=200)
        else:
            return JsonResponse(aperturapost_serializer.errors, status=400)