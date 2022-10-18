import os
import sys
import time

from WS4_SQL import db_connect, db_disconnect, db_create
from Wallapop_Selenium import boton_cookies, start_selenium, selenium_close, guardar_datos, guardar_datos_sql, scroll
from WS4_art import banner,colores

global busqueda
global categoria
global max_price
global min_price
max_price = None
min_price = None
busqueda = None
categoria = None

def menu():
    cls()

    print(banner)
    print("[1] Set búsqueda")
    print("[2] Set categoria")
    print("[3] Buscar")
    print("[4] Crear Estadistica")
    print("[0] Salir")

    try:
        global opcion
        opcion = int(input("\n"))
    except:
        print("¡Introduce un número!")
        time.sleep(2)
        menu()
    else:
        cls()
        opciones()

def cls():
    os.system("cls")

def iniciar():
    print(banner)
    if busqueda != None and categoria != None and busqueda != "" and busqueda != " ": # Comprobamos que se hayan modificado los valores iniciales de las variables para evitar errores
        tabla = busqueda.replace(" ", "_") # Reemplazamos los espacios para el titulo de la tabla por "_"
        # tabla2 = tabla + "_trash"
        start_selenium(url)
        cls()
        print(banner)
        boton_cookies()
        scroll()
        guardar_datos(categoria)
        db_connect()
        db_create(tabla)
        # db_create(tabla2)
        guardar_datos_sql(busqueda, tabla, categoria)
        selenium_close()
        db_disconnect()
        input(f"\n{colores.OKBLUE}Pulsa Cualquier Tecla Para Continuar{colores.ENDC}")
        
        menu()
    else:
        print(f"{colores.WARNING}¡Comprueba que has especificado la búsqueda y la categoría!{colores.ENDC}")
        time.sleep(2)
        menu()

def menu_categoria():
    global categoria
    print(banner)
    print("[1] Motos")
    print("[2] Coches")
    print("[3] Motor y Accesorios")
    print("[4] Volver")
    print("[5] Salir")
    while True:
        global categoria_input
        try:
            categoria_input = int(input("\n"))
        except:
            print("¡Introduce un valor válido!")
            time.sleep(3)
        else:
            if categoria_input >= 1 and categoria_input <=5:
                if categoria_input == 1:
                    categoria = 14000
                elif categoria_input == 2:
                    categoria = 100
                elif categoria_input == 3:
                    categoria = 12800
                elif categoria_input == 4:
                    continue
                elif categoria_input == 5:
                    sys. exit()
                global url
                url = f"https://es.wallapop.com/app/search?keywords={busqueda}&category_ids={categoria}&filters_source=seo_landing&latitude=41.38804&longitude=2.17001"
                menu()
            else:
                wrong_number()
                cls()
                menu_categoria()
            
def menu_busqueda():
    global busqueda
    global url
    print(banner)
    busqueda = input("Introduce tus terminos de búsqueda\n")
    url = f"https://es.wallapop.com/app/search?keywords={busqueda}&category_ids={categoria}&filters_source=seo_landing&latitude=41.38804&longitude=2.17001"
    menu()
        
def opciones():
    if opcion == 1:
        menu_busqueda()
    elif opcion == 2:
        menu_categoria()
    elif opcion == 3:
        iniciar()
    elif opcion == 4:
        print("")
    elif opcion == 0:
        sys.exit()
    else:
        wrong_number()
        menu()

def parametros(): # En construcción
    print(banner)
    print("[1] Rango de Precio")
    print("[2] Ubicación")
    print("[3] Distancia")
    print("[4] Volver")
    print("[5] Salir")
    parametro = input()
    
    while True:
        if parametro >=1 and parametro <= 5:
            if parametro == 1:
                cls()
                print(banner)
                print("Rango Actual:")
                print("[1] Máxmino")
                print("[2] Minimo")
                print("[3] Volver")
                print("[4] Reestablecer")

            elif parametro == 2:
                print
            elif parametro == 3:
                print
            elif parametro == 4:
                continue
            elif parametro == 5:
                sys.exit
            menu()
        else:
            wrong_number()
            cls()
            parametros()

def wrong_number():
    print(f"{colores.WARNING}¡Introduce un número dentro de los valores permitidos!{colores.ENDC}")
    time.sleep(3)

menu()