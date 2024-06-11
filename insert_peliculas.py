import csv
import re
import mysql.connector

# Conexión a la base de datos
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="peliculas"
)

cursor = conn.cursor()

# Función para limpiar el score
def limpiarScore(score):
    match = re.search(r"([\d,.]+)", score)
    if match:
        return float(match.group(0).replace(",", "."))
    else:
        return None

# Ruta al archivo CSV
csvFile = 'movies_data.csv'

try:
    with open(csvFile, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=',')
        next(csv_reader)  # Ignorar la primera fila (encabezado)
        for row in csv_reader:
            titulo = row[0]
            duracion = row[1]
            puntuacion = limpiarScore(row[2])
            descripcion = row[3]
            lanzamiento = row[4]

            sql = "INSERT INTO peliculas (titulo, descripcion, duracion, score, lanzamiento) VALUES (%s, %s, %s, %s, %s)"
            values = (titulo, descripcion, duracion, puntuacion, lanzamiento)

            cursor.execute(sql, values)
            print("Datos insertados correctamente en la tabla de películas.")
except Exception as e:
    print(f"Error al insertar datos: {e}")
finally:
    conn.commit()
    conn.close()
