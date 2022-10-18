from datetime import datetime

maxyear = int(datetime.today().strftime('%Y'))
minyear = int(2000)

def aislar_ano(descripcion):
    puntuacion_texto = [".", ",", "-", "_", ":", ";", '"', "'"]    
    for simbolo in puntuacion_texto:
        descripcion = descripcion.replace(simbolo," ") # Eliminamos Cualquier simbolo que pueda crear problemas a la hora de buscar / insertar datos en la DB

    descripcion = descripcion.split()

    # print(descripcion)
    
    for a in range (minyear,maxyear,1):
        if str(a) in descripcion:
            ano = a
            break
        else:
            ano = -1
    return ano

    