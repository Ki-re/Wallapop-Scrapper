from difflib import SequenceMatcher


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# def similar_words(busqueda,titulo):
#     busqueda = str(busqueda.lower)
#     titulo = str(titulo.lower)

#     busqueda = busqueda.split()
#     titulo = titulo.split()

#     match = list(set(busqueda) & set(titulo)) # Obtenemos las coincidencias entre los strings
#     return int(len(match)) # Devolvemos el número de coincidencias


def similar_words(busqueda, titulo):
    # Convertimos los valores en string y eliminamos las mayusculas
    # print(busqueda)
    # print(titulo)
    
    busqueda = str(busqueda.lower())
    titulo = str(titulo.lower())

    titulo_split = titulo.split()

    puntuacion_texto = ["-", "/"]

    for simbolo in puntuacion_texto:
        busqueda = busqueda.replace(simbolo,"") # Eliminamos Cualquier simbolo que pueda crear problemas a la hora de buscar / insertar datos en la DB
        titulo = titulo.replace(simbolo,"") # Eliminamos Cualquier simbolo que pueda crear problemas a la hora de buscar / insertar datos en la DB


    # print(titulo_split)
    # print(busqueda)

    # Si existe una coincidencia entre el titulo y la busqueda directamente se aporta un valor SI (1)
    if busqueda in titulo_split == True:
        return True
    elif titulo.replace(" ", "").find(busqueda.replace(" ", "")) > -1:
        return True
    elif len(list(set(busqueda) & set(titulo))) > len(titulo)/3:
        return True
    else:
        return False
