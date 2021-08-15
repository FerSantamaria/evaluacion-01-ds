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
    
    for key, value in document_columns.items():
        new_ce[key] = input(f"{value}: ")
    
    inserted_ce = conn.insert_one(new_ce)
    print(f"\n{inserted_ce}")


def update(conn):
    print("Edición")

def delete(conn):
    print("Eliminación")

def read(conn):
    print("Consulta")

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

# Clearing terminal screen and displaying user menu
clear_screen()

while True: 
    print("===== Administracion de Centros Escolares =====\n")
    print("Opciones:")
    print("1. Registrar")
    print("2. Editar")
    print("3. Eliminar")
    print("4. Consultar catálogo")
    print("5. Créditos")
    print("6. Salir")

    selected_option = input("\nElija una opción: ")

    try:
        selected_option = int(selected_option)
    except ValueError:
        selected_option = 0

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