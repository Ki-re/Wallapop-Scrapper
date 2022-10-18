import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from datetime import datetime
import WS4_Credenciales as credenciales

def db_connect():
    try:
        global connection
        connection = mysql.connector.connect( # Configuración de la conexión con la base de datos
            host= credenciales.host,
            database= credenciales.database,
            user= credenciales.user,
            password= credenciales.password)
    except Error as error:
        print("Se ha roto")
        print("Error while connecting to MySQL", error)
        input()
        db_connect()
    else:
        print("Conexión DB Realizada Correctamente")
        
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version", db_Info)
            global cursor
            # cursor = connection.cursor()
            cursor = connection.cursor(buffered=True)


def db_create(tabla):
    try: 
        cursor.execute(f"create table if not exists {tabla} (id int not null, fecha_datos date not null,hora time not null, titulo varchar(150), precio int,km int, ano bigint,descripcion text,link varchar(200), categoria int, primary key(id, fecha_datos, hora))")
    except Error as err:
        print(f"Ha ocurrido un error al intentar crear la tabla: {err}")
    else:
        print(f"Tabla {tabla} creada") 

def db_insert(tabla, precio, titulo, descripcion, link_anuncio, id, km, year, categoria): # Se debe realizar la llamada de introducción de datos especificando los valores obtenidos durante el Scraping
    fecha = datetime.today().strftime('%Y-%m-%d')
    hora = datetime.today().strftime('%H:%M:%S')
    while True:
        try:
            linea = f"insert into {tabla} (id, fecha_datos, hora, precio, titulo, descripcion, link, km, ano, categoria) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (id, fecha, hora, precio, titulo, f"{descripcion}", link_anuncio, f"{km}", f"{year}", f"{categoria}")
            cursor.execute(linea, val)
            connection.commit()
        except Error as err:
            if err.errno == 1062: # Error de primary key
                print("Primary key ya en la DB")
                input() # To-do
            else:
                print("Error al introducir los datos en la DB")
                print(f"\nError:{err.errno}")
                print(f"\nError:{err.msg}")
                print(f"\nError:{err.args}")
                input() # Pausa
        else:
            print("Datos Insertados Correctamente")
            break

def lineas():
    return cursor.rowcount

def db_disconnect():
    cursor.close()
    connection.close()
    print("Conexión DB Cerrada Existosamente")

def busqueda(termino_busqueda): # Se debe realizar la llamada de la función especificando de que tabla se quieren obtener los datos
    comando = f"select id,precio,km from {termino_busqueda}"
    cursor.execute(comando)
    return cursor.fetchall()

def anuncios_year(termino_busqueda):
    comando = f"select DISTINCT ano from {termino_busqueda} where ano > 2000 order by ano asc;"
    cursor.execute(comando)
    return cursor.fetchall()

def media_precio_km(termino_busqueda, year):
    comando = f"select avg(precio)/avg(km) from {termino_busqueda} where km > 100 and precio > 500 and ano = {year};"
    cursor.execute(comando)
    return cursor.fetchall()

def numero_auncios(termino_busqueda):
    comando = f"select count(id) from {termino_busqueda} where km > 100 and precio > 500;"
    cursor.execute(comando)
    return cursor.fetchall()

def db_create_estadistica(tabla):
    tabla = tabla+"_estadistica"
    try: 
        cursor.execute(f"create table if not exists {tabla} (busqueda varchar(100) not null,ano int not null,preciokm decimal (6,2), primary key(busqueda, ano))")
    except Error as err:
        print(f"Ha ocurrido un error al intentar crear la tabla: {err}")
    else:
        print(f"Tabla {tabla} creada") 

def db_update_estadistica(tabla,ano,preciokm):
    titulo_tabla = tabla+"_estadistica"
    
    linea = f"update {titulo_tabla} SET preciokm = {preciokm} where busqueda = {tabla} VALUES (%s, %s, %s)"
    val = (tabla, ano, preciokm)
    cursor.execute(linea, val)
    connection.commit()

def db_insert_estadistica(tabla,ano,preciokm):
    titulo_tabla = tabla+"_estadistica"
    
    try:
        linea = f"insert into {titulo_tabla} (busqueda, ano, preciokm) VALUES (%s, %s, %s)"
        val = (tabla, ano, preciokm)
        cursor.execute(linea, val)
        connection.commit()
    except Error as err:
        if err.errno == 1062: # Error de primary key
            print("Primary key ya en la DB")
            db_update_estadistica(tabla,ano,preciokm)
            # input() # To-do
        else:
            print("Error al introducir los datos en la DB")
            print(f"\nError:{err.errno}")
            print(f"\nError:{err.msg}")
            print(f"\nError:{err.args}")
            # input() # Pausa
    else:
        print("Datos Insertados Correctamente")

def db_encontrar_tablas():
    try:
        linea = "show tables;"
        cursor.execute(linea)
    except Error as err:
        pass
    else:
        return cursor.fetchall()

def db_select_categoria(tabla):
    try:
        linea = f"select distinct(categoria) from {tabla};"
        cursor.execute(linea)
    except Error as err:
        print(err)
        pass
    else:
        return cursor.fetchall()