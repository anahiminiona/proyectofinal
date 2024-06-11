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
            generos = row[5]

            pelicula_id = obtenerIdPelicula(conn, titulo)

            sql = "INSERT INTO generos (genero, id_pelicula) VALUES (%s, %s)"
            cursor.execute(sql, (generos, pelicula_id))
            print("Datos insertados correctamente en la tabla de géneros.")
except Exception as e:
    print(f"Error al insertar datos: {e}")
finally:
    conn.commit()
    conn.close()