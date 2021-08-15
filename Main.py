#Developed by Fernando Santamaría
#https://github.com/FerSantamaria
#2021-15-08

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

#New document method
def new(conn):
    new_ce = {}

    print("===== Registro =====\n")
    
    for key, value in document_columns.items():
        new_ce[key] = input(f"{value}: ")

        if key == "_id":
            numeric = False
            unique = False     

            # Making sure id is numeric and unique
            while not numeric or not unique:
                numeric = is_numeric(new_ce[key])
                
                if not numeric:
                    new_ce[key]= input("ERROR: El valor del Id debe ser numérico, ingrese un nuevo valor\nId: ")

                else:
                    unique = is_unique(conn, new_ce[key])

                    if not unique:
                        new_ce[key]= input("ERROR: El valor del Id se encuentra en uso, ingrese un nuevo valor\nId: ")
    
    new_ce["_id"] = int(new_ce["_id"])
    conn.insert_one(new_ce)

    print(f"\nRegistro insertado con éxito")

def is_numeric(id):
    return id.isnumeric()

def is_unique(conn, id):
    return True if conn.find_one({"_id": int(id)}) is None else False

#Update document method
def update(conn):
    print("===== Actualización =====\n")
    search_id = input("Ingrese el Id del centro escolar a editar: ")

    if is_numeric(search_id):
        current_ce = conn.find_one({"_id": int(search_id)})

        if current_ce is not None:
            print("\nSi no desea realizar algún cambio, solo presione enter a cada uno de los campos que se le presentarán a continuación")
        
            for key, value in document_columns.items():
                if key != "_id":
                    new_value = input(f"Nuevo {value} (Actual: {current_ce[key]}): ")
                    current_ce[key] = current_ce[key] if not new_value else new_value
            
            conn.update_one({"_id": int(search_id)}, {"$set" : current_ce})

            print(f"\nRegistro actualizado con éxito")

        else: 
            print(f"\nNo se encontró ningún registro con ese Id ({search_id})")

    else: 
        print(f"\nId no válido")

# Delete document method
def delete(conn):
    print("===== Eliminación =====\n")
    search_id = input("Ingrese el Id del centro escolar a eliminar: ")

    if is_numeric(search_id):
        current_ce = conn.find_one({"_id": int(search_id)})

        if current_ce is not None:         
            current_ce_data = [data for data in conn.find({"_id": int(search_id)})]
            print("\n")
            print_data(current_ce_data)

            conn.delete_one({"_id": int(search_id)})
            print(f"\nRegistro eliminado con éxito")

        else: 
            print(f"\nNo se encontró ningún registro con ese Id ({search_id})")

    else: 
        print(f"\nId no válido")

# Read all documents method
def read(conn):
    print("===== Catálogo =====\n")
    
    catalog_data = [data for data in conn.find()]
    print_data(catalog_data)

#Developer's information method
def credits(conn):
    print("Desarrollado por: José Fernando Flores Santamaría")
    print("https://github.com/FerSantamaria/evaluacion-01-ds")

#Prints formatted data using pandas
def print_data(data):
    dataframe = pd.DataFrame(data).rename(columns=document_columns).set_index('Id')
    print(dataframe)

#Clear screen utility
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear') 

#Menu options methods dictionary
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