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

# Leer datos de la tabla
cur.execute("SELECT * FROM nombres;")
registros = cur.fetchall()

print("Nombres en la tabla:")
for registro in registros:
    print(registro)
# Registrar la operación en la tabla de log
cur.execute("INSERT INTO log_operaciones (operacion, nodo_actual) VALUES (%s, %s)", ('READ', 'nodo_1'))

# Confirmar los cambios en la base de datos
conn.commit()


# Cerrar conexión
cur.close()
conn.close()

