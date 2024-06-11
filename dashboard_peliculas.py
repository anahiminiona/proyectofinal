import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_table
from dash import Dash, html, dcc
import mysql.connector

# Función para obtener la conexión a la base de datos
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="peliculas"
    )
    return conn

# Función para obtener los datos de películas
def get_movies_data():
    conn = get_db_connection()
    query = "SELECT * FROM peliculas"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Función para obtener los directores de una película
def get_directors(movie_id):
    conn = get_db_connection()
    query = "SELECT directores FROM directores WHERE id_pelicula = %s"
    cursor = conn.cursor()
    cursor.execute(query, (movie_id,))
    directors = [row[0] for row in cursor.fetchall()]
    conn.close()
    return ', '.join(directors)

# Función para obtener la película más popular y menos popular
def get_popularity_data():
    conn = get_db_connection()
    most_popular_query = "SELECT titulo, score FROM peliculas ORDER BY score DESC LIMIT 1"
    least_popular_query = "SELECT titulo, score FROM peliculas ORDER BY score ASC LIMIT 1"
    
    most_popular = pd.read_sql(most_popular_query, conn)
    least_popular = pd.read_sql(least_popular_query, conn)
    
    conn.close()
    return most_popular, least_popular

# Función para obtener la película más larga y más corta
def get_duration_data():
    conn = get_db_connection()
    longest_movie_query = "SELECT titulo, duracion FROM peliculas ORDER BY duracion DESC LIMIT 1"
    shortest_movie_query = "SELECT titulo, duracion FROM peliculas ORDER BY duracion ASC LIMIT 1"
    
    longest_movie = pd.read_sql(longest_movie_query, conn)
    shortest_movie = pd.read_sql(shortest_movie_query, conn)
    
    conn.close()
    return longest_movie, shortest_movie

def create_dashboard(data: pd.DataFrame):
    most_popular, least_popular = get_popularity_data()
    longest_movie, shortest_movie = get_duration_data()

    fig_histogram = px.histogram(data, x="score", title="Distribución de Puntuaciones")

    # Obtener los directores para cada película
    data['directores'] = data['id'].apply(get_directors)

    body = html.Div([
        html.H2("Dashboard de Películas", style={"textAlign": "center", "color": "blue"}),
        html.P("Objetivo: Mostrar datos de películas almacenadas en la base de datos."),
        html.Hr(),
        dbc.Row([
            dbc.Col(dcc.Graph(id="histogramPlot", figure=fig_histogram), width=12),
        ]),
        html.H3("Película Más Popular", style={"textAlign": "center", "color": "green"}),
        html.P(f"Título: {most_popular['titulo'].values[0]}, Puntuación: {most_popular['score'].values[0]}"),
        html.H3("Película Menos Popular", style={"textAlign": "center", "color": "red"}),
        html.P(f"Título: {least_popular['titulo'].values[0]}, Puntuación: {least_popular['score'].values[0]}"),
        html.H3("Película Más Larga", style={"textAlign": "center", "color": "green"}),
        html.P(f"Título: {longest_movie['titulo'].values[0]}, Duración: {longest_movie['duracion'].values[0]}"),
        html.H3("Película Más Corta", style={"textAlign": "center", "color": "red"})
        html.P(f"Título: {shortest_movie['titulo'].values[0]}, Duración: {shortest_movie['duracion'].values[0]}"),
        html.H3("Películas y Directores", style={"textAlign": "center", "color": "blue"}),
        dash_table.DataTable(
            id='table',
            columns=[
                {'name': 'ID', 'id': 'id'},
                {'name': 'Título', 'id': 'titulo'},
                {'name': 'Directores', 'id': 'directores'},
                {'name': 'Duración', 'id': 'duracion'},
                {'name': 'Lanzamiento', 'id': 'lanzamiento'},
                {'name': 'Score', 'id': 'score'}
            ],
            data=data.to_dict('records'),
            sort_action='native',
            style_table={'overflowX': 'auto'},
        ),
    ])

    return body

# Obtener los datos de películas
movies_data = get_movies_data()

# Crear la aplicación Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = create_dashboard(movies_data)

if __name__ == "__main__":
    app.run_server(debug=True)
