import csv
import mysql.connector

# Conexión a la base de datos
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="peliculas"
)

cursor = conn.cursor()

# Ruta al archivo CSV
csvFile = 'movies_data.csv'

# Función para obtener el ID de la película
def obtenerIdPelicula(conn, titulo):
    sql = "SELECT id FROM peliculas WHERE titulo = %s"
    cursor.execute(sql, (titulo,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        print(f"Error: No se encontró la película '{titulo}'.")
        return None

try:
    with open(csvFile, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=',')
        next(csv_reader)  # Ignorar la primera fila (encabezado)
        for row in csv_reader:
            titulo = row[0]
            directores = set(row[6].split(","))  # Dividir los directores por coma y eliminar duplicados
            directores = [director.strip() for director in directores]  # Eliminar espacios en blanco alrededor de los directores

            pelicula_id = obtenerIdPelicula(conn, titulo)

            # Verificar si los directores ya han sido insertados para esta película
            directores_insertados = set()
            sql = "SELECT directores FROM directores WHERE id_pelicula = %s"
            cursor.execute(sql, (pelicula_id,))
            for result in cursor.fetchall():
                directores_insertados.update(result[0].split(","))

            for director in directores:
                if director not in directores_insertados:
                    # Insertar el director en la tabla de directores
                    sql = "INSERT INTO directores (directores, id_pelicula) VALUES (%s, %s)"
                    cursor.execute(sql, (director, pelicula_id))
                    print(f"Dato insertado correctamente en la tabla de directores para la película '{titulo}': {director}")
                    directores_insertados.add(director)

except Exception as e:
    print(f"Error al insertar datos: {e}")
finally:
    conn.commit()
    conn.close()
