from WS4_SQL import anuncios_year,media_precio_km



def crear_estadistica(termino_busqueda):

    anos = anuncios_year(termino_busqueda) # Determinamos los años de la busqueda

    for ano in anos:
        precio_medio_km = media_precio_km(termino_busqueda,ano) # Obtenemos el precio medio de los KM diferenciando por año

        