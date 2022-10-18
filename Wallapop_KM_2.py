def limpiar_input(input_text,year):
    input_text = input_text.lower() # Eliminamos las mayusculas del texto

    simbolos_limpiar = [".", ",", "_", ":", ";", '"', "'","(",")"]
    terminos_sustituir = [" mil", "mil"]

    input_text.replace("000km", "000 km")

    if year > 0:
        input_text = input_text.replace(str(year),"")

    for termino in terminos_sustituir:
        if input_text.find(termino) > -1: # Buscamos un posible valor "mil" para sustituirlo por 000 de forma que el valor sea numerico
                try:
                    input_text = input_text.replace(termino, "000")
                except:
                    continue

    for simbolo in simbolos_limpiar:
        try: # Controlamos cualquier posible error en caso de que el termino no exista en el texto
            input_text = input_text.replace(simbolo,"") # Eliminamos Cualquier simbolo que pueda crear problemas a la hora de buscar / insertar datos en la DB
        except:
            continue
    
    return input_text

def encontrar_termino(input_text,year):
    descripcion_anuncio = limpiar_input(input_text,year) # Limpiamos el input que recibimos
    find = 0 # Iniciamos la variable find en 0, esta se encargará de marcar el número de veces que se encuentren los terimnos en el texto
    terminos_busqueda = ["kilometros", "kilómetros", "km", "klm"] # Determinamos los terminos de busqueda que usaremos para identificar la presencia de un valor de km en el texto
    
    for termino in terminos_busqueda:
        if descripcion_anuncio.find(termino) > -1:
            find += 1
            termino_encontrado = termino
            descripcion_anuncio = descripcion_anuncio.replace(termino, " "+termino+" ")
    
    descripcion_anuncio = descripcion_anuncio.split()
    
    try:
        descripcion_anuncio = descripcion_anuncio.remove(" ")
    except:
        pass
    
    # Devolvemos un valor según si se ha encontrado alguno de los terminos en el texo o no, este booleano determinará si se procede a la busqueda de un valor númerico o se pasa al siguiente anuncio 
    if find > 0:
        print("Se han encontrado KM")
        descripcion_anuncio.append(descripcion_anuncio.index(termino_encontrado))
        descripcion_anuncio.append("1")
    elif find == 0:
        print("No se han encontrado KM")
        descripcion_anuncio.append("0")
    return descripcion_anuncio
    
def encontrar_numero(input_text, year):
    texto = encontrar_termino(input_text, year)

    km = -1
    posicion_km = -1

    if str(texto[-2]).isnumeric() == True:
        posicion_km = int(texto[-2])
    
    try:
        texto[posicion_km+3] # Comprobamos que dentro del texto sea posible comprobar las 3 posiciones anteriores y posteriores al termino "km"
        texto[posicion_km-3]
    except:
        posicion_km = -1 # En caso de que no existan las 3 posiciones anteriores/posteriores comprobamos todo el texto
    
    if texto[-1] == "1" and posicion_km != -1:
        for a in range (posicion_km-3, posicion_km+3):
            if str(texto[a]).isnumeric() == True and int(texto[a]) > int(km):
                km = texto[a]
    elif texto[-1] == "1" and posicion_km == -1:
        for a in range (len(texto)):
            if str(texto[a]).isnumeric() == True and int(texto[a]) > int(km):
                km = texto[a]
    return km
