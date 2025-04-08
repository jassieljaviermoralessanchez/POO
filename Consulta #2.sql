SHOW  ENGINES;


SHOW VARIABLES;


SET default_storage_engine='InnoDB';



CREATE DATABASE IF NOT EXISTS gestion_tareas CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE gestion_tareas;


CREATE TABLE IF NOT EXISTS materias (
    id INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS tareas (
    id INT NOT NULL AUTO_INCREMENT,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT,
    fecha_entrega DATE NOT NULL,
    estado ENUM('pendiente', 'completado') NOT NULL DEFAULT 'pendiente',
    materia_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (materia_id) REFERENCES materias(id) ON DELETE CASCADE
);

SHOW TABLES;

SHOW DATABASES;





