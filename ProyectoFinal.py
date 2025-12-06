import os
from func_apoyo import *
from Funcion_bd import *

# seria el inicio del programa si no tuvieramos una base de datos definida 
def inicion_pro()-> str:
    """
    Mediante un input pide el nombre de la base de datos que queremos utilizar y luego se utiliza la funcion conec_crear_bd() para crear o conectar la base de datos\n
    return:
        base_datos(str): Nombre de la base de datos que se creo o conecto
    """
    while True:
        base_datos = obtener_datos("la base de datos con la que quiere trabajar")[0]
        conec_crear_bd(base_datos)
        break 
    return base_datos

# =========== Programa principal ==============# 
def programa_principal(archivo_db):
    conec_crear_bd(archivo_db)
    while True:
        print("="*45)
        print(f"Trabajando en la base de datos|{archivo_db}|")
        print("="*45)
        opcionun = obtener_datos(f"la opcion deseada:\n1.Utilizar tabla ya existente\n2.Crear nueva tabla\n3.Salir\n{"="*45} \n")[0]
        opcionun= int(opcionun)
        match opcionun:
            case 1:
                if len(ver_tablas(archivo_db))==0:
                    print("\n[ERROR]No se encontro tablas en su base de datos!!!\n")    
                else:
                    while True:
                        print(f"Estas son las tablas existentes en su base de datos: \n{ver_tablas(archivo_db)}")
                        opcion = obtener_datos("la tabla con la que desea trabajar: ")[0]
                        if opcion in ver_tablas(archivo_db):
                            print(f"\nTrabajando en la tabla |{opcion}|")
                            opciones_primMenu(archivo_db,opcion)
                            break
                        else:
                            print("\n[ERROR]Ingrese una tabla existente\n")
            case 2:
                crear_tabla(archivo_db)
            case 3:
                return print("===Fin del programa===")               

#=== Es el menu que se ejecurara luego de establecer la tablas con la que se trabajara ===#
def opciones_primMenu(archivo_db,tabla_nomb):
    
    while True:
        mostrar_menuprimero()
        opc_menuprim = (obtener_datos("la opcion deseada: "))

        match int(opc_menuprim[0]):
            case 1:
                opcion_menuprod(archivo_db,tabla_nomb)
            case 2:
                repot_stock(archivo_db,tabla_nomb)
            case 3:
                ver_tabla(archivo_db,tabla_nomb)
            case 4:
                break

#=== El menu de productos se ejecuta se se selecciona la opcio "1" del menu principal
def opcion_menuprod(archivo_db,tabla_nomb):
    while True:
        mostrar_menuproduc()
        opc_eleg = (obtener_datos("la opcion deseada: "))

        match int(opc_eleg[0]):
            case 1:
                actualizar_datos(archivo_db,tabla_nomb)
            case 2:
                eliminar_producto(archivo_db,tabla_nomb)
            case 3:
                agregar_producto(archivo_db,tabla_nomb)
            case 4:
                buscar_producto(archivo_db,tabla_nomb)
            case 5:
                return

def main():
    
    os.chdir(os.path.dirname(__file__))

    #archivo_db = inicion_pro()
    archivo_db = "inventario.db"
    #tabla_nomb = "productos"
    programa_principal(archivo_db)
    
if __name__ == "__main__":
    main()