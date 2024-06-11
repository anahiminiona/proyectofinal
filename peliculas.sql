CREATE DATABASE IF NOT EXISTS peliculas;

USE peliculas;

CREATE TABLE IF NOT EXISTS peliculas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT,
    duracion VARCHAR(20),
    score FLOAT,
    lanzamiento INT
);

CREATE TABLE IF NOT EXISTS generos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    genero VARCHAR(100) NOT NULL,
    id_pelicula INT,
    FOREIGN KEY (id_pelicula) REFERENCES peliculas(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS directores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    directores VARCHAR(255) NOT NULL,
    id_pelicula INT,
    FOREIGN KEY (id_pelicula) REFERENCES peliculas(id) ON DELETE CASCADE
);