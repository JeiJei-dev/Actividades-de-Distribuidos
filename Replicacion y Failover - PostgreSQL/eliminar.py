import psycopg2
from psycopg2 import sql
import argparse
import schedule
import time
import random

# Configuración de la conexión a la base de datos
db_config = {
    'host': '192.168.1.106',
    'database': 'postgres',
    'user': 'postgres'
}

# Conectar a la base de datos
conn = psycopg2.connect(**db_config)
cur = conn.cursor()

def eliminar_nombres():
    cur.execute("DELETE FROM nombres;")
    cur.execute("INSERT INTO log_operaciones (operacion, nodo_actual) VALUES (%s, %s)", ('DELETE', 'nodo_1'))
    # Confirmar los cambios en la base de datos
    print("Eliminado nombres")
    conn.commit()

def eliminar_log():
    cur.execute("DELETE FROM log_operaciones;")
    cur.execute("INSERT INTO log_operaciones (operacion, nodo_actual) VALUES (%s, %s)", ('DELETE', 'nodo_1'))
    # Confirmar los cambios en la base de datos
    print("Eliminado log")
    conn.commit()

def eliminar_id_log(iD):
    cur.execute("DELETE FROM log_operaciones WHERE id = %s", (iD,))
    cur.execute("INSERT INTO log_operaciones (operacion, nodo_actual) VALUES (%s, %s)", ('DELETE', 'nodo_1'))
    # Confirmar los cambios en la base de datos
    print("Eliminado log id:",(iD,))
    conn.commit()

def eliminar_id_nombre(iD):
    cur.execute("DELETE FROM nombres WHERE id = %s", (iD,))
    cur.execute("INSERT INTO log_operaciones (operacion, nodo_actual) VALUES (%s, %s)", ('DELETE', 'nodo_1'))
    # Confirmar los cambios en la base de datos
    print("Eliminado nombre id:",(iD,))
    conn.commit()

def mostrar_menu():
    # Configuración de la conexión a la base de datos
    db_config = {
        'host': '192.168.1.106',
        'database': 'postgres',
        'user': 'postgres'
    }

    # Conectar a la base de datos
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()

    while True:
        print("\n--- Menú ---")
        print("1. Eliminar nombre por ID")
        print("2. Eliminar log por ID")
        print("3. Eliminar todos los logs")
        print("4. Eliminar todos los nombres")
        print("5. Salir")

        opcion = input("Selecciona una opción (1-5): ")

        if opcion == '1':
            id_nombre = input("Ingresa el ID del nombre a eliminar: ")
            eliminar_id_nombre(id_nombre)
        
        elif opcion == '2':
            id_log = input("Ingresa el ID del log a eliminar: ")
            eliminar_id_log(id_log)

        elif opcion == '3':
            eliminar_log()

        elif opcion == '4':
            eliminar_nombres()

        elif opcion == '5':
            print("Saliendo del programa...")
            # Cerrar conexión
            cur.close()
            conn.close()
            break
        
        else:
            print("Opción no válida. Por favor, selecciona una opción entre 1 y 5.")

if __name__ == "__main__":
    mostrar_menu()

