from WS4_SQL import db_connect, db_encontrar_tablas, db_select_categoria, db_disconnect
from Wallapop_Selenium import start_selenium, boton_cookies, scroll, guardar_datos, guardar_datos_sql, selenium_close
import time

# Esta parte del código se encarga de buscar las tablas ya creadas (las búsquedas ya realizadas) y las actualiza para aumentar el volumen de datos

limpiar_select = ["(",")","'",",","[","]"]

while True:
    try:
        db_connect()
    except Exception as e:
        print("Error:")
        print(e)
    else:
        busquedas = db_encontrar_tablas() # Obtenemos los nombres de todas las tablas, por ende de todas las busquedas que hay que actualizar
        for busqueda in busquedas: # Iteramos entre las distintas búsquedas
            busqueda = str(busqueda)
            
            for simbolo in limpiar_select:
                busqueda = busqueda.replace(simbolo,"")
            
            categoria = str(db_select_categoria(busqueda))
            
            for simbolo in limpiar_select:
                categoria = (categoria.replace(simbolo,""))
            
            tabla = busqueda
            busqueda = busqueda.replace("_"," ")

            url = f"https://es.wallapop.com/app/search?keywords={busqueda}&category_ids={categoria}&filters_source=seo_landing&latitude=41.38804&longitude=2.17001"

            categoria = int(categoria)

            start_selenium(url)
            boton_cookies()
            scroll()
            guardar_datos(categoria)
            guardar_datos_sql(busqueda, tabla, categoria)
            selenium_close()
        
        db_disconnect()

    time.sleep((3600*6))