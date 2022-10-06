import psycopg2
import os
import time
connlocal = None
cursorlocal=None
total=0

SERVIDOR_LOCAL=os.environ.get('URL_SERVIDOR')

######################################
#############ACCESOS###################
#######################################
acceso1=os.environ.get('URL_ACCESO1')
acceso2=os.environ.get('URL_ACCESO2')
acceso3=os.environ.get('URL_ACCESO3')
acceso4=os.environ.get('URL_ACCESO4')

descripcion_acceso1=os.environ.get('RAZON_ACCESO1')
descripcion_acceso2=os.environ.get('RAZON_ACCESO2')
descripcion_acceso3=os.environ.get('RAZON_ACCESO3')
descripcion_acceso4=os.environ.get('RAZON_ACCESO4')


dispositivos=[acceso1, acceso2, acceso3, acceso4,
              SERVIDOR_LOCAL,
              ]

dispositivos_dict ={acceso1:descripcion_acceso1, 
                    acceso2:descripcion_acceso2, 
                    acceso3:descripcion_acceso3, 
                    acceso4:descripcion_acceso4, 
                    SERVIDOR_LOCAL:'SERVIDOR LOCAL',
                    }

while True:
    
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


        
        cursorlocal.execute('CREATE TABLE IF NOT EXISTS dias_acumulados (fecha varchar(150))')
        cursorlocal.execute('CREATE TABLE IF NOT EXISTS web_dispositivos (dispositivo varchar(150), descripcion varchar(150), estado varchar(150))')
        connlocal.commit()

        cursorlocal.execute('SELECT*FROM web_dispositivos')
        tabladispositivos= cursorlocal.fetchall()

       

        if len(tabladispositivos) < 1:
            for dispositivo in dispositivos:
                if dispositivo:
                    descripcion = dispositivos_dict[dispositivo]
                    if dispositivo == SERVIDOR_LOCAL:
                        estado = '1'
                    else:
                        estado = '0'
                    cursorlocal.execute('INSERT INTO web_dispositivos values(%s, %s, %s)',(dispositivo, descripcion, estado))
                    connlocal.commit()

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
        break
    
