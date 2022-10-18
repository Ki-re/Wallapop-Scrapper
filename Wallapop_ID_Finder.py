def aislar_link_imagen(enlace_imagen,titulo_anuncio):
    link = enlace_imagen.replace("/", " ")
    link = link.split()
    link = link[-2]
    id = link.replace("c10420p","")

    sustituir = ["- ", " - ", " -", " ", "/"]

    titulo = titulo_anuncio.lower()
    titulo = titulo.replace("  ", " ")
    
    for item in sustituir:
        titulo = titulo.replace(item, "-")
    
    link_anuncio = "https://es.wallapop.com/item/"+titulo+"-"+id

    resultado = [id,link_anuncio]

    return resultado
