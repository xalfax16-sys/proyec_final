import os
import sqlite3
from func_apoyo import *

def crear_conex_cursor(archivo_db:str):
    """
    Crea la conexion y cursor al archivo.db indicado\n
    args:
        archivo_db(str): Nombre de la base de datos
    return:
        objeto: tuple
    """
    conexion = sqlite3.connect(archivo_db)
    cursor = conexion.cursor()
    return conexion,cursor    

def ver_tablas(archivo_db:str)->list:
    """
    Muestra el nombre de todas las tablas que se encuentran en la base de datos indicado
    omitiendo la tabla "sqlite_sequence"(predeterminada de SQLite)\n
    args:
        archivo_db(str): Nombre de la base de datos
    return:
        objeto: list
    """
    conexion,cursor = crear_conex_cursor(archivo_db)
    cursor.execute(f"""SELECT name FROM sqlite_master WHERE type="table" """)
    lista = cursor.fetchall()
    conexion.close()
    tablas = []
    # tablas =[tabla[0] for tabla in cursor.fetchall()]
    for tabla in lista:
        nomb_tabla = tabla[0]
        if nomb_tabla=="sqlite_sequence":
            continue
        else:
            tablas.append(nomb_tabla)
    
    return tablas

def validar_tablas(archivo_db:str,tabla_nomb:str)->bool:
    """
    Valida si la tabla ingresada se encuentra en la base de datos\n
    args:
        archivo_db(str): Nombre de la base de datos
        tabla_nomb(str): Nombre de la tabla a validar
    return:
        objeto: bool
    """
    tablas = ver_tablas(archivo_db)
    
    return tabla_nomb in tablas

def ver_columna(archivo_db:str,tabla_nomb:str):
    """
    Muestra los encabezado de la tabla indicada\n
    args:
        archivo_db(str): Nombre de la base de datos
        tabla_nomb(str): Nombre de la tabla 
    return:
        list: Columnas existentes
    """
    conexion,cursor = crear_conex_cursor(archivo_db)
    cursor.execute(f"""PRAGMA table_info({tabla_nomb})""")
    columnas_exis = [colum[1] for colum in cursor.fetchall()]
    conexion.close()
    
    return columnas_exis

def validar_columna(archivo_db:str,tabla_nomb:str,columna:str)->bool:
    """
    Valida si la columna ingresada se encuentra en la tabla\n
    args:
        archivo_db(str): Nombre de la base de datos
        tabla_nomb(str): Nombre de la tabla 
        columna(str): nombre de la columna a validar
    return:
        bool
    """
    columnas_exis = ver_columna(archivo_db,tabla_nomb)
    
    return columna in columnas_exis
#==========================================================================================#
def conec_crear_bd(archivo_db:str):#
    """
    Crea o conecta una base de datos .db\n
    args:
        archivo_db(str): Nombre de la base de datos
    """
    conexion = sqlite3.connect(archivo_db)
    conexion.close()

def crear_tabla(archivo_db:str):#
    """
    Crea una tabla en la base de datos señalado\n
    columnas:"id","nombre","descripcion","cantidad","precio","categoria".
    args:
        archivo_db(str): Nombre de la base de datos
    """
    conexion,cursor = crear_conex_cursor(archivo_db)
    tabla_nomb = obtener_datos("el nombre de la tabla que desea crear: ")[0]
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS "{tabla_nomb}"(
                "id" INTEGER NOT NULL UNIQUE,
	            "nombre" TEXT NOT NULL,
                "descripcion" TEXT NOT NULL,
                "cantidad" INTEGER NOT NULL,
	            "precio" REAL NOT NULL,
                "categoria" TEXT,
	            PRIMARY KEY("id" AUTOINCREMENT))
                """)
    conexion.commit()
    conexion.close()
    return print("===Tabla creada con exito===")

def ver_tabla(archivo_db:str,tabla_nomb):#
    """
    Muestra la tabla indicada\n
    args:
        archivo_db(str): Nombre de la base de datos
        tabla_nomb(str): Nombre de la tabla 
    """
    conexion,cursor = crear_conex_cursor(archivo_db) 
    cursor.execute(f"""SELECT * FROM {tabla_nomb}""")
    encabe = ver_columna(archivo_db,tabla_nomb)
    tabla = cursor.fetchall()
    conexion.close()
    print(f"=========Taba {tabla_nomb}=========")
    for fila in tabla:
        print(F"{encabe[0]}:{fila[0]} / {encabe[1]}:{fila[1]} / {encabe[2]}:{fila[2]} / {encabe[3]}:{fila[3]} / {encabe[4]}:{fila[4]} / {encabe[5]}:{fila[5]}")
    return 
        
def agregar_producto(archivo_db:str,tabla_nomb:str):#
    """
    Agrega filas a la tabla indicada los datos se pedirian medianta la funciono obtener_datos()\n
    args:
        archivo_db(str): Nombre de la base de datos
        tabla_nomb(str): Nombre de la tabla
    """
    nombre,descripcion,cantidad,precio,categoria = obtener_datos(
    "el nombre: ","la descripcion: ","el stock : ","el precio : ","la categoria: ")
    conexion,cursor = crear_conex_cursor(archivo_db)
    cursor.execute(f"INSERT INTO {tabla_nomb} (nombre,descripcion,cantidad,precio,categoria) VALUES (?,?,?,?,?)",
    (nombre,descripcion,cantidad,precio,categoria))
    conexion.commit()
    conexion.close()
    
    print(f"\nnombre:{nombre} descripcion:{descripcion} cantidad:{cantidad} precio:{precio} categoria:{categoria}")
    print(f"\n|El producto se agrego correctamente|")
    
    return 

def buscar_producto(archivo_db:str,tabla_nomb:str):#
    """
    Muestra registros indicado, segun "id", "nombre" o "categoria"\n
    Los datos ingresados seran validados segun correspondan mediante las funciones\n
    validar_datos_str, validar_datos_float, validar_datos_int\n
    args:
        archivo_db(str): Nombre de la base de datos
        tabla_nomb(str): Nombre de la tabla
    """
    while True:
        colum =input("\nRealizar busqueda segun:\n1.id\n2.nombre\n3.categoria\n")
        if validar_dato_int(colum):
            colum = int(colum)
        match colum:
            case 1:
                columna = "id"
                break
            case 2:
                columna = "nombre"
                break
            case 3:
                columna = "categoria"
                break
    if columna =="id":
            dato = obtener_datos("la id del producto que desea buscar: ")[0]
            dato = int(dato)
    else:
        dato = obtener_datos("el dato que desea buscar: ")[0]
    
    conexion,cursor = crear_conex_cursor(archivo_db)
    cursor.execute(f"""SELECT * FROM {tabla_nomb} WHERE {columna} = ?""", (dato,))
    resultado = cursor.fetchall()
    conexion.close()
    if len(resultado)==0:
        return print("\n[ERROR]No se encontro el productos")
    else:
        id_result = []
        print("#===Estos son los productos encontrados:===#\n")
        for dato in resultado:
            print(f"#id:{dato[0]} nombre:{dato[1]} descripcion:{dato[2]} cantidad:{dato[3]} precio:{dato[4]} categoria:{dato[5]}")
            id_result.append(dato[0])
    return
#########################################################################################

        # opcion= obtener_datos("la opcion a realizar:\n1.Actualiza dato\n2.Eliminar producto\n3.Atras\n")[0]
        # opcion = int(opcion)
        # match opcion:
        #     case 1:
        #         return actualizar_datos(archivo_db,tabla_nomb)
        #     case 2:
        #         return eliminar_producto(archivo_db,tabla_nomb)
        #     case 3:
        #         return

def actualizar_datos(archivo_db:str,tabla_nomb:str):#
    """
    Actualiza registros a la tabla indicada, los datos nesesarios se pedirian mediante la funcion obtener_datos()\n
    esta funcion primero busca y muestra el producto que desa actualizar luego se pide confirmar la accion\n
    si se confirma pesira la columna donde se desea actualizar(esta columna sera validada por la funcion validar_columna())\n
    args:
        archivo_db(str): Nombre de la base de datos
        tabla_nomb(str): Nombre de la tabla
    """
    pk = obtener_datos("la id del producto a actualizar: ")[0]
    conexion,cursor = crear_conex_cursor(archivo_db)
    colum_pk = "id"
    
    cursor.execute(f"""SELECT * FROM {tabla_nomb} WHERE {colum_pk} = ?""", (pk,))
    hola = cursor.fetchall()
    if len(hola) == 0:
        return print("\n[ERROR]No se encontro el productos")
    else:    
        for dato in hola:
            print("\n=======Producto encontrado=======")
            print(f"id:{dato[0]} nombre:{dato[1]} descripcion:{dato[2]} cantidad:{dato[3]} precio:{dato[4]} categoria:{dato[5]}\n")
    
    while True:
        opcion = obtener_datos("la opcion deseada: \n1.Actualizar dato\n2.Cancelar\n")[0]
        opcion= int(opcion)
        match opcion:
            case 1:
                columna = obtener_datos("la columna donde se actualizara: ")[0]
                if validar_columna(archivo_db,tabla_nomb,columna):
                    nuevo_dato = obtener_datos("el nuevo dato: ")[0]
                    cursor.execute(f"""UPDATE {tabla_nomb} SET {columna} = ? WHERE {colum_pk} = ? """,(nuevo_dato,pk))
                    conexion.commit()
                    conexion.close
                    return print("\nEl producto se actualizo correctamente")
                else:
                    print("\n[ERROR]La columna ingresada no existe\n")    
            case 2:
                conexion.close
                return
    
def eliminar_producto(archivo_db:str,tabla_nomb:str):#
    """
    Elimina registros a la tabla indicada, los datos nesesarios se pedirian mediante la funcion obtener_datos()\n
    esta funcion primero busca y muestra el producto que desa actualizar luego se pide confirmar la accion\n
    args:
        archivo_db(str): Nombre de la base de datos
        tabla_nomb(str): Nombre de la tabla
    """
    id_producto = obtener_datos("la id del producto a eliminar: ")[0]
    columna = "id"
    conexion,cursor = crear_conex_cursor(archivo_db)
    cursor.execute(f"""SELECT * FROM {tabla_nomb} WHERE {columna} = ?""", (id_producto,))
    resul = cursor.fetchall()
    
    if len(resul)==0:
        return print("\n[ERROR]No se a encontrado productos con esa id")
    else:
        print(f"\n=====Producto econtrado=====\n{resul[0]}\n")
    
    while True:
        opcion = obtener_datos("la opcion a realizar: \n1.confirmar\n2.cancelar\n")[0]
        opcion = int(opcion)
        if  opcion== 1:
            cursor.execute(f"""DELETE FROM {tabla_nomb} WHERE {columna} = ?""", (id_producto,))
            conexion.commit()
            print("==Producto eliminado con exito==")
        conexion.close()
        return

def repot_stock(archivo_db:str,tabla_nomb:str):#
    """
    Muestra los registros donde el stock <= al limite indicado, los datos se pediran mediante la funcion obtener_datos()\n
    args:
        archivo_db(str): Nombre de la base de datos
        tabla_nomb(str): Nombre de la tabla
    """
    limite = obtener_datos("el minimo stock aceptado: ")[0]
    conexion,cursor = crear_conex_cursor(archivo_db)
    columna = "cantidad"
    cursor.execute(f"""SELECT * FROM {tabla_nomb} WHERE {columna} <= ?""",(limite,))
    poco_stock = cursor.fetchall()
    conexion.close 
    if len(poco_stock)==0:
        return print("\n##No hay productos con poco stock##")
    else:
        print("=====Estos son los productos con poco stock=====\n")
        for dato in poco_stock:
                print(f"id:{dato[0]} nombre:{dato[1]} descripcion:{dato[2]} cantidad:{dato[3]} precio:{dato[4]} categoria:{dato[5]}")

def main():
    
    os.chdir(os.path.dirname(__file__))

if __name__ == "__main__":
    main()


    