from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome import options
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver

from WS4_comparator import similar_words
from WS4_SQL import db_insert
from WS4_art import banner
from Wallapop_KM_2 import encontrar_numero
from Wallapop_Year import aislar_ano
from Wallapop_ID_Finder import aislar_link_imagen

import time
import os
from WS4_art import colores

opciones = Options()
scroll_distance = 1000

opciones.headless = True
opciones.add_argument("--incognito")
opciones.add_argument('log-level=3')
# opciones.add_argument('--remote-debugging-port=9222')
opciones.add_argument('--window-size=1920,1080')

def start_selenium(url):
    # Inicialización del navegador de selenium
    global navegador
    navegador = webdriver.Chrome(options=opciones) 
    # if opciones.headless == False:
    #     navegador.minimize_window()
    navegador.implicitly_wait(2)
    navegador.get(url)
    time.sleep(2)


def boton_cookies():
    if opciones.headless == False: # Solo buscamos el botón de cookies si selenium se encuentra en headless (false)
        for a in range(5): # El for tiene 5 iteraciones que buscan el botón para aceptar la cookies.
            try:
                boton_cookies = navegador.find_element(By.ID, "didomi-notice-agree-button")
            except NoSuchElementException:
                print(f"\n{colores.WARNING}No se ha encontrado un botón de cookies{colores.ENDC}")
            else:
                boton_cookies.click()
                print(f"\n{colores.OKGREEN}Botón Cookies Correcto{colores.ENDC}")
                break

def scroll():
    offset_scroll = -(scroll_distance*4) # Añadimos un offset negativo para dar cierto margen de carga en caso de conexión lenta
    salir = False # Variable que controla el While
    
    while salir == False: # Este bucle controla el scroll hasta el final de la página, funciona con un try que ejecuta la busqueda del botón de "ver más", si no lo encuentra se controla la excepción y el programa scrollea hacia abajo una cantidad determinada más arriba
        try:
            boton_ver_mas = navegador.find_element(By.ID, "btn-load-more")
        except NoSuchElementException:
            navegador.execute_script(f"window.scrollBy(0,{scroll_distance})")
            print(f"\n{colores.OKGREEN}Scroll correcto de {scroll_distance}px{colores.ENDC}")

            height = navegador.execute_script('return window.pageYOffset')
            print(height)
                
            offset_scroll += scroll_distance
            print(offset_scroll)
            
            if offset_scroll > height:
                salir = True
                print(f"\n{colores.OKCYAN}Scroll Terminado{colores.ENDC}")
                break
        else:
            boton_ver_mas.click()
            print(f"\n{colores.OKGREEN}Botón Ver Más Correcto{colores.ENDC}")
    print(f"\n{colores.OKBLUE}Página descargada correctamente{colores.ENDC}")

def guardar_datos(categoria):
    # Guardamos los datos en las variables (listas)
    global anuncios
    global precios
    global titulos
    global descripciones
    global imagenes
    if categoria == 14000: # Motos
        print(f"{colores.OKBLUE}    Anuncios Motos{colores.ENDC}")
        anuncios = navegador.find_elements(By.CLASS_NAME, "ItemCardList__item")
        precios = navegador.find_elements(By.CLASS_NAME, "ItemCard__price")
        titulos = navegador.find_elements(By.CLASS_NAME, "ItemCard__title")
        descripciones = navegador.find_elements(By.CLASS_NAME, "ItemCard__description")
        imagenes = navegador.find_elements(By.CLASS_NAME, "ItemCard__image")
    elif categoria == 100: # Coches
        print(f"{colores.OKBLUE}    Anuncios Coches{colores.ENDC}")
        anuncios = navegador.find_elements(By.CLASS_NAME, "ItemCardList__item")
        precios = navegador.find_elements(By.CLASS_NAME, "ItemCardWide__price")
        titulos = navegador.find_elements(By.CLASS_NAME, "ItemCardWide__title")
        descripciones = navegador.find_elements(By.CLASS_NAME, "ItemCardWide__description")

def guardar_datos_sql(busqueda, tabla, categoria):
    anuncio_guardado = 0
    anuncio_deshechado = 0
    for a in range(len(anuncios)): # Iteramos entre una de las listas (anuncios) para almacenar todos los elementos de las listas

        imagen = imagenes[a].find_element(By.TAG_NAME, "img") # Obtenemos el contenedor de la imagen del anuncio en cada iteración
        link_imagen = imagen.get_attribute("src")
                
        finder = aislar_link_imagen(link_imagen, titulos[a].text) # LLamamos a la función aislar_link_imagen que nos devuelve una lista con el enlace y la ID del anuncio
        
        link_anuncio = finder[1] # Separamos la lista finder en el enlace y la ID del anuncio
        id = finder[0]
        
        # Declaramos el precio actual
        try:
            precio = precios[a].text
        except:
            print(f"No se ha podido obtener el precio del anuncio nº{a}")
            precio = None
        else:
            precio = precio.replace("€",'') # Sustituimos el punto y el simbolo del € de cara a la DB
            precio = precio.replace("$",'')
            precio = precio.replace(".",'')
            precio = precio.replace(",",'')

        # Declaramos el titulo actual
        try:
            titulo = titulos[a].text
        except:
            print(f"No se ha podido obtener el titulo del anuncio nº{a}")
            titulo = None
        
        # Declaramos la descripción actual
        try:
            descripcion = descripciones[a].text
            descripcion = descripcion.replace('"',"")
            descripcion = descripcion.replace("'","") # Encerramos las descripciones entre triples comillas para evitar que posibles comillas en el texto lanzen una excepción
            #print(descripcion)
        except:
            print(f"No se ha podido obtener la descripion del anuncio nº{a}")
            descripcion = None          
        else:
            try:
                puntuacion_texto = [".", ",", "-", "_", ":", ";", '"', "'"]
                for simbolo in puntuacion_texto:
                    texto = texto.strip(simbolo) # Eliminamos Cualquier simbolo que pueda crear problemas a la hora de buscar / insertar datos en la DB
            except:
                pass

        match = similar_words(busqueda, titulo)
        ano = aislar_ano(descripcion)

        if (match == True):

            anuncio_guardado +=1
        
            km = encontrar_numero(descripcion,ano)
        
            try:
                print(precio)
                db_insert(tabla, precio, titulo, descripcion, link_anuncio, id, km, ano, categoria)
            except:
                print("Fallo al introducir en la db")
                continue
        else:
            anuncio_deshechado += 1
        os.system("cls")
        print(banner)
        print(f"Progreso: ({colores.OKGREEN}{anuncio_guardado} correctos{colores.ENDC}/{colores.WARNING}{anuncio_deshechado} deshechados{colores.ENDC})")

    print(f"Encontrados {anuncio_deshechado+anuncio_guardado+1} anuncios") # Printamos el contador con un +1 dado que se ha inicializado en -1

def selenium_close():
    navegador.close() # Cerramos el navegador de selenium