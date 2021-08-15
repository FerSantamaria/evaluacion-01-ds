import pandas as pd
import pymongo
import os

def get_connection():
    client = pymongo.MongoClient("mongodb+srv://FerSanDev:SPpz7EoG9P2TNbEt@datascience.0ujvz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    
    my_db = client["Evaluacion01"]
    my_collection = my_db["CE"]

    return my_collection

document_columns = {
    "_id" : "Id",
    "name": "Nombre",
    "state": "Departamento",
    "town": "Municipio"
}

def new(conn):
    new_ce = {}

    print("===== Registro =====\n")
    s
    for key, value in document_columns.items():

        new_ce[key] = input(f"{value}: ")

        if key == "_id":
            numeric = False
            unique = False     

            while not numeric or not unique:
                numeric = is_numeric(new_ce[key])
                
                if not numeric:
                    new_ce[key]= input("ERROR: El valor del Id debe ser numérico, ingrese un nuevo valor\nId: ")

                else:
                    unique = is_unique(conn, new_ce[key])

                    if not unique:
                        new_ce[key]= input("ERROR: El valor del Id se encuentra en uso, ingrese un nuevo valor\nId: ")
    
    new_ce["_id"] = int(new_ce["_id"])

    inserted_ce = conn.insert_one(new_ce)
    print(f"\nRegistro insertado con éxito")

def is_numeric(id):
    return id.isnumeric()

def is_unique(conn, id):
    return True if conn.find_one({"_id": int(id)}) is None else False

def update(conn):
    print("===== Actualización =====\n")
    
def delete(conn):
    print("Eliminación")

def read(conn):
    print("===== Catálogo =====\n")
    
    catalog_data = [data for data in conn.find()]
    df_catalog_data = pd.DataFrame(catalog_data).rename(columns=document_columns).set_index('Id', )
    print(df_catalog_data)
    

def credits(conn):
    print("Desarrollado por: José Fernando Santamaría")
    print("https://github.com/FerSantamaria/evaluacion-01-ds")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear') 

menu_options = {
    1: new,
    2: update,
    3: delete,
    4: read,
    5: credits,
}

# ============= Main Program =============

while True: 
    # Clearing terminal screen and displaying user menu
    clear_screen()

    print("===== Administracion de Centros Escolares =====\n")
    print("Opciones:")
    print("1. Registrar")
    print("2. Editar")
    print("3. Eliminar")
    print("4. Consultar catálogo")
    print("5. Créditos")
    print("6. Salir")

    selected_option = input("\nElija una opción: ")

    selected_option = int(selected_option) if selected_option.isnumeric() else 0

    if selected_option >=1 and selected_option <= 5:
        clear_screen()

        conn = get_connection()
        menu_options[int(selected_option)](conn)

        input("\nPresione enter para continuar...")
        clear_screen()
    elif selected_option == 6:
        print("\nTerminando ejecución")
        break
    else:
        input("\nOpción inválida. Presione enter para reintentar...")