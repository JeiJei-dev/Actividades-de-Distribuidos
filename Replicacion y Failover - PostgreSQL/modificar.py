import psycopg2

def modificar_nombre(id_nombre, nuevo_nombre):
    # Configuración de la conexión a la base de datos
    db_config = {
        'host': '192.168.1.106',
        'database': 'postgres',
        'user': 'postgres'
    }

    # Conectar a la base de datos
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()


    try:
        cur = conn.cursor()
        
        # Comando para modificar el nombre por ID
        cur.execute("UPDATE nombres SET nombre = %s WHERE id = %s;", (nuevo_nombre, id_nombre))
        
        # Confirmar los cambios en la base de datos
        conn.commit()
        
        if cur.rowcount > 0:
            print(f"Nombre con ID '{id_nombre}' modificado exitosamente a '{nuevo_nombre}'.")
        else:
            print(f"No se encontró un nombre con ID '{id_nombre}'.")

    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        cur.close()
        conn.close()

# Ejemplo de uso
if __name__ == "__main__":
    id_a_modificar = input("Ingresa el ID del nombre a modificar: ")
    nuevo_nombre = input("Ingresa el nuevo nombre: ")
    
    modificar_nombre(id_a_modificar, nuevo_nombre)
