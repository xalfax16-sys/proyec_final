import os

def pedir_db():
    base_datos = obtener_datos("la base de datos con la que quiere trabajar")[0]
    return base_datos

def mostrar_menuprimero():
    print("="*20)
    print("   |MENU PRINCIPAL|")
    print("="*20)
    print("1.Menu productos")
    print("2.Report stock")
    print("3.Ver tabla")
    print("4.Volver")
    print("="*20)

def mostrar_menuproduc():
    print("="*30)
    print("      |MENU PRODUCTOS|")
    print("="*30)
    print("1.Actualizar producto")
    print("2.Eliminar producto")
    print("3.Agregar producto")
    print("4.Buscar producto")
    print("5.Volver")
    print("="*30)

def obtener_datos(*cant_datos):
    """
    Pide datos (la misma cantidad de veces como cantidad de argumetos,cada argumento se sumara al input para completar la oracion)\n
    ["Ingrese {arg}: "]y los almacena en una lista\n
    Los datos ingresados seran validados segun correspondan mediante las funciones\n
    validar_datos_str, validar_datos_float, validar_datos_int\n
    args:
        *cant_datos:
    return:
        list
    """
    datos_ingre = []

    for tex in cant_datos:
        while True:
            dato = input(f"Ingrese {tex}").strip().lower()
            dato_validado = def_tipo_val(tex,dato)
            if dato_validado is True:
                datos_ingre.append(dato)
                break 
    return datos_ingre 

def validar_datos_str(dato):
    """
    Valida que se haya ingresado el dato\n
        args:
        dato(str): Dato a validar
    """
    if dato == "":
        print("[ERROR]Ingrese el dato pedido\n")
        return None
    return True

def validar_dato_float(dato):
    """
    Valida que que el dato ingresado sea un float positivo\n
    no se transforma el dato\n
        args:
        dato(str): Dato a validar
    """
    try:
        numeor = float(dato)
        if numeor >= 0:
            return True
        return print("[ERROR]El dato debe ser un numero positivo\n")
            
    except ValueError:
            print("[ERROR]Dato incorrecto\n")
    except BaseException:
            print("[ERROR INESPERADO]\n")

def validar_dato_int(dato):
    """
    Valida que que el dato ingresado sea un int positivo\n
    no se transforma el dato\n
        args:
        dato(str): Dato a validar
    """
    try:
        numeor = int(dato)
        if numeor >= 0:
            return True
        return print("[ERROR]El dato debe ser un numero positivo\n")
            
    except ValueError:
            print("[ERROR]Dato incorrecto\n")
    except BaseException:
            print("[ERROR INESPERADO]\n")

def def_tipo_val(tex,dato):
    """
    Inspecciona el texto ingresado y evalua si se encuentran las palabras cavles\n
    segun esto define si se debe validar como str, int o float\n
    si el texto tiene "precio" validara float
    si el texto tiene ["id","cantidad","opcion","stock"] validara int
        args:
        dato(str): Dato a validar
    """
    pal_claves = "precio"
    pal_clav_ = ["id","cantidad","opcion","stock"]
    
    if pal_claves in tex.split():
        return validar_dato_float(dato)
    for palabra in pal_clav_:  
        if palabra in tex.split():
            return validar_dato_int(dato)
    return validar_datos_str(dato)    

def main():
    
    os.chdir(os.path.dirname(__file__))
    
    mostrar_menuproduc()
    
if __name__ == "__main__":
    main()