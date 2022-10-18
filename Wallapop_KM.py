# def aislar_km(descripcion):
#     texto = descripcion.lower()

#     busqueda = ["km ","kilometros ", "kilómetros ", "kms "]
#     find = 0

#     for termino in busqueda: # Buscamos la presencia de uno de los terminos
#         if texto.find(termino) > -1:
#             find += 1
#             # posicion_km = texto.find(termino)
#             text_split = texto.split()
#             termino = termino.replace(" ","") # Reemplazamos el espacio añadido para establecer la busqueda de los terminos completos
#             posicion_km = text_split.index(termino)
            
#     if find == 1: # Comparamos los resultados obtenidos en la busqueda
#         print("Se han encontrado KM")
#         km = text_split[posicion_km-1]
#     elif find == 0:
#         print("No hay KMS")
#         km = None
#     elif find > 1:
#         print("Se ha encontrado un conflicto, más de un valor km")
#         km = None


def aislar_km(descripcion, ano):
    texto = descripcion.lower()
    puntuacion_texto = [".", ",", "_", ":", ";", '"', "'","(",")"]

    if texto.find(" mil") > -1: # Buscamos un posible valor "mil" para sustituirlo por 000 de forma que el valor sea numerico
        texto = texto.replace(" mil","000")
    
    if texto.find("mil") > -1: # Buscamos un posible valor "mil" para sustituirlo por 000 de forma que el valor sea numerico
        texto = texto.replace("mil","000")

    for simbolo in puntuacion_texto:
        texto = texto.replace(simbolo,"") # Eliminamos Cualquier simbolo que pueda crear problemas a la hora de buscar / insertar datos en la DB

    busqueda = ["kilometros", "kilómetros", "km"]
    find = 0
    km = -1 # Iniciamos la variable km en -1 para determinarlo como valor nulo

    for termino in busqueda: # Buscamos la presencia de uno de los terminos
        if texto.find(termino) > -1: # Buscamos uno por uno los terminos de la lista "busqueda" y sumamos una unidad a la variable find en caso de encontrar un resultado
            find += 1
            texto = texto.replace(termino, f" {termino} ") # Añadimos un espacio antes y despues de "km" para aislar el posible número colindante
            termino_encontrado = termino
            #texto = texto.replace(str(ano),f" {str(ano)} ")

    if find == 1: # Comparamos los resultados obtenidos en la busqueda
        print("Se han encontrado KM")

        text_split = texto.split() # Creamos una lista a partir del texto
            
        if int(ano) != -1 and ano in text_split: # Eliminamos el año
            ano = str(ano)
            text_split = text_split.remove(ano)

        try: # Eliminamos cualquier item formado por un espacio en blanco
            text_split = text_split.remove(" ") 
        except:
            pass
        print(text_split)
        
        posicion_km = text_split.index(termino_encontrado) # Obtenemos la posición del termino "km" en la lista

        #print(text_split)

        aumento = 3
        decremento = -2

        try: # Comprobamos que existen elementos por encima y por debajo del termino "km"
            text_split[posicion_km+decremento]
        except:
            decremento = 0
        try:
            text_split[posicion_km+aumento]
        except:
            aumento = 0

        if posicion_km != -1:
            for a in range (posicion_km+decremento, posicion_km+aumento):  # Buscamos en las 2 posiciones anteriores y las 2 posteriores al valor "km" para encontrar el valor numerico más grande
                if text_split[a] == False:
                    for letra in text_split[a]:
                        if letra.isnumeric() == True:
                            for letra2 in letra:
                                if letra2.isnumeric() == False:
                                    letra = letra.replace(letra2,"")
                try:
                    num_actual_list = str(text_split[a].isnumeric())
                except:
                    num_actual_list = False
                if num_actual_list == True:
                    numero = int(text_split[a])
                    if numero > km:
                        km = numero   
            # km = text_split[posicion_km-1]
            # km = km.replace(".","")
            # km = km.replace(",","")
        
        if str(km).isnumeric() == False: # Comprobamos que el valor sea numerico, en caso contrario, otorgramos un valor de -1 para evitar un error al introducir los datos en la db
            km = -1
    
    elif find == 0:
        print("No hay KMS")
        km = -1
    elif find > 1:
        print("Se ha encontrado un conflicto, más de un valor km")
        km = -1
    
    return km # Devolvemos el valor "km", en caso de no haber encontrado será igual a -1 y en caso de haber encontrado un valor "km" el resultado se basará en la busqueda