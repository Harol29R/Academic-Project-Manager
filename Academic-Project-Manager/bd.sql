CREATE DATABASE trabajos_db;

USE trabajos_db;

CREATE TABLE trabajos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo_trabajo VARCHAR(255),
    tipo_trabajo VARCHAR(50),
    autor VARCHAR(100),
    universidad VARCHAR(150),
    palabras_claves TEXT,
    resumen TEXT,
    curso VARCHAR(50),
    imagen LONGBLOB,
    pdf VARCHAR(255),
    ciudad VARCHAR(100),
    especialidad VARCHAR(50)
);