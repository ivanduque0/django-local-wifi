import psycopg2
import os
import time
from ping3 import ping

CONTRATO=os.environ.get("CONTRATO")
connlocal = None
cursorlocal=None
total=0
total_ping = 0
TIEMPO_PING=int(os.environ.get('TIEMPO_PING'))

######################################
#############ACCESOS###################
#######################################
acceso1=os.environ.get('URL_ACCESO1')
acceso2=os.environ.get('URL_ACCESO2')
acceso3=os.environ.get('URL_ACCESO3')
acceso4=os.environ.get('URL_ACCESO4')

dispositivos=[acceso1, acceso2, acceso3, acceso4, 
              ]

#EN caso que hayan mas dispositivos, se les agregan mas ceros a la lista intentos
intentos=[0,0,0,0]

while True:
    total=0
    t1=time.perf_counter()
    while total<=5:
        t2=time.perf_counter()
        total=t2-t1
    total=0
    try:
        
        #con esto se apunta a la base de datos local
        connlocal = psycopg2.connect(
            database=os.environ.get("SQL_DATABASE"), 
            user=os.environ.get("SQL_USER"), 
            password=os.environ.get("SQL_PASSWORD"), 
            host=os.environ.get("SQL_HOST"), 
            port=os.environ.get("SQL_PORT")
        )
        cursorlocal = connlocal.cursor()
        
        
        t1_ping=time.perf_counter()
        while True:
            t2_ping=time.perf_counter()
            total_ping=t2_ping-t1_ping

            # ESTE ES EL TIEMPO EN EL QUE SE HACE PING A LOS DISPOSITIVOS, 
            # LO NORMAL PARA PRODUCCION SON 2 MINUTOS
            if total_ping > TIEMPO_PING:
                for dispositivo in dispositivos:
                    intentos_tabla=dispositivos.index(dispositivo)
                    if dispositivo:
                        longitud_url=len(dispositivo)
                        ping_dispositivo = ping(dispositivo[7:longitud_url])
                        if ping_dispositivo:
                            cursorlocal.execute('UPDATE web_dispositivos SET estado=1 WHERE dispositivo=%s', (dispositivo,))
                            connlocal.commit()
                            intentos[intentos_tabla]=0
                        else:
                            intentos[intentos_tabla]=intentos[intentos_tabla]+1
                            if intentos[intentos_tabla] >= 4:
                                cursorlocal.execute('UPDATE web_dispositivos SET estado=0 WHERE dispositivo=%s', (dispositivo,))
                                connlocal.commit()
                t1_ping=time.perf_counter()


    except (Exception, psycopg2.Error) as error:
        print("fallo en hacer las consultas")
        if connlocal:
            cursorlocal.close()
            connlocal.close()
    finally:
        print("se ha cerrado la conexion a la base de datos")
        if connlocal:
            cursorlocal.close()
            connlocal.close()
