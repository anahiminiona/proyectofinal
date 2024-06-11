from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv

# Configuración del WebDriver
chrome_options = Options()
chrome_options.add_argument("--log-level=3")
driver = webdriver.Chrome(options=chrome_options)

def load_more_movies():
    try:
        for _ in range(5):  # Hacemos clic 5 veces para cargar 300 películas
            see_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., '50 más')]"))
            )
            driver.execute_script("arguments[0].click();", see_more_button)
            time.sleep(5)  # Espera para que las nuevas películas se carguen
    except Exception as e:
        print(f"Error al cargar más películas: {e}")

def get_movie_details(movie_url):
    driver.get(f'https://m.imdb.com{movie_url}')
    time.sleep(3)  # Espera para que se cargue la página completamente

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Extraer géneros
    genres = [genre_tag.text.strip() for genre_tag in soup.select('div.ipc-chip-list__scroller a span.ipc-chip__text')]
    
    # Extraer director(es)
    directors = [director_tag.text.strip() for director_tag in soup.select('li[data-testid="title-pc-principal-credit"] span:contains("Dirección") + div ul li a')]
    
    return genres, directors

def get_movies_info(url):
    driver.get(url)
    time.sleep(5)  # Espera para que se cargue la página completamente

    load_more_movies()

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    movies = []

    for item in soup.find_all('li', class_='ipc-metadata-list-summary-item'):
        title_tag = item.find('h3', class_='ipc-title__text')
        metadata_tags = item.find_all('span', class_='sc-b189961a-8 kLaxqf dli-title-metadata-item')
        score_tag = item.find('span', class_='ipc-rating-star--imdb')
        description_tag = item.find('div', class_='ipc-html-content-inner-div')
        link_tag = item.find('a', class_='ipc-title-link-wrapper')
        
        title = title_tag.text.strip().split(".")[1].strip() if title_tag else 'N/A'
        release_year = metadata_tags[0].text.strip() if len(metadata_tags) > 0 else 'N/A'
        duration = metadata_tags[1].text.strip() if len(metadata_tags) > 1 else 'N/A'
        score = score_tag.text.strip().split(" ")[0] if score_tag else 'N/A'
        description = description_tag.text.strip() if description_tag else 'N/A'
        link = link_tag['href'] if link_tag else 'N/A'
        
        # Verificar que el formato de duración sea válido (contiene 'h' y 'm')
        if 'h' in duration and 'm' in duration:
            if title != 'N/A' and score != 'N/A' and description != 'N/A' and link != 'N/A':
                genres, directors = get_movie_details(link)
                movies.append({
                    'title': title,
                    'duration': duration,
                    'score': score,
                    'description': description,
                    'release_year': release_year,
                    'genres': ', '.join(genres),
                    'directors': ', '.join(directors)
                })

    return movies

# URL específica
url = 'https://m.imdb.com/search/title/?release_date=2023-01-01,&genres=horror'
movies_info = get_movies_info(url)

# Filtrar y limitar las películas a 250 si hay más
filtered_movies = movies_info[:250]

# Definir la ruta del archivo CSV
csv_file = 'movies_data.csv'

# Abrir el archivo CSV en modo escritura
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    # Crear el escritor CSV
    writer = csv.DictWriter(file, fieldnames=['Título', 'Duración', 'Puntuación', 'Descripción', 'Año de Lanzamiento', 'Géneros', 'Directores'])
    
    # Escribir los encabezados
    writer.writeheader()
    
    # Escribir cada fila de datos
    for movie in filtered_movies:
        writer.writerow({'Título': movie['title'],
                         'Duración': movie['duration'],
                         'Puntuación': movie['score'],
                         'Descripción': movie['description'],
                         'Año de Lanzamiento': movie['release_year'],
                         'Géneros': movie['genres'],
                         'Directores': movie['directors']})

print(f"Se han guardado las películas en el archivo: {csv_file}")

# Mostrar las películas por consola
for idx, movie in enumerate(filtered_movies, start=1):
    print(f"Título: {idx}. {movie['title']}")
    print(f"Duración: {movie['duration']}")
    print(f"Puntuación: {movie['score']}")
    print(f"Descripción: {movie['description']}")
    print(f"Año de Lanzamiento: {movie['release_year']}")
    print(f"Géneros: {movie['genres']}")
    print(f"Directores: {movie['directors']}")
    print("-" * 20)

driver.quit()
