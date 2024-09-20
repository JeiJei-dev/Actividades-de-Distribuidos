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

# Crear tablas si no existen
cur.execute("""
CREATE TABLE IF NOT EXISTS nombres (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS log_operaciones (
    id SERIAL PRIMARY KEY,
    operacion VARCHAR(255) NOT NULL,
    nodo_actual VARCHAR(100) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

# Función para insertar un nombre y registrar la operación
def insertar_nombre(nombre, nodo_actual):
    # Insertar nombre en la tabla de nombres
    cur.execute("INSERT INTO nombres (nombre) VALUES (%s)", (nombre,))
    
    # Registrar la operación en la tabla de log
    cur.execute("INSERT INTO log_operaciones (operacion, nodo_actual) VALUES (%s, %s)",
                ('INSERT', nodo_actual))
    
    # Confirmar los cambios en la base de datos
    conn.commit()

def generar_nombre_aleatorio():
    # Listas de nombres y apellidos
    nombres = ["Juan", "María", "Pedro", "Ana", "Luis", "Laura", "Carlos", "Elena"]
    apellidos = ["García", "Pérez", "López", "Martínez", "Sánchez", "Rodríguez", "Gómez"]

    # Seleccionar un nombre y un apellido aleatorios
    nombre = random.choice(nombres)
    apellido = random.choice(apellidos)

    # Devolver el nombre completo
    return f"{nombre} {apellido}"

# Ejemplo de uso
for i in range(10):
    insertar_nombre(generar_nombre_aleatorio(), 'nodo_1')  # Llama a la función
    print("inserción: %i",i)
    time.sleep(2)  # Espera 2 segundos antes de la siguiente ejecución


# Cerrar conexión
cur.close()
conn.close()
