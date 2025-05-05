-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS bibliolexis;
USE bibliolexis;

-- Create usuarios (users) table
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    nombre_usuario VARCHAR(50) UNIQUE NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    rol VARCHAR(20) DEFAULT 'usuario',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create libros (books) table
CREATE TABLE IF NOT EXISTS libros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    autor VARCHAR(200) NOT NULL,
    editorial VARCHAR(100),
    anio VARCHAR(4),
    isbn VARCHAR(20) UNIQUE,
    genero VARCHAR(50),
    sinopsis TEXT,
    disponibles INT DEFAULT 1,
    total INT DEFAULT 1,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create prestamos (loans) table
CREATE TABLE IF NOT EXISTS prestamos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    libro_id INT NOT NULL,
    fecha_prestamo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_devolucion TIMESTAMP NOT NULL,
    fecha_devolucion_real TIMESTAMP NULL,
    estado VARCHAR(20) DEFAULT 'prestado',
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (libro_id) REFERENCES libros(id)
);

-- Create default admin user
INSERT INTO usuarios (nombre, apellido, nombre_usuario, correo, telefono, contrasena, rol)
SELECT 'Administrador', 'Sistema', 'admin', 'admin@bibliolexis.com', '0000000000', 
       'sha256$GENERATED_HASH', 'admin'
WHERE NOT EXISTS (
    SELECT 1 FROM usuarios WHERE nombre_usuario = 'admin'
);

-- Create some sample books
INSERT INTO libros (titulo, autor, editorial, anio, isbn, genero, sinopsis, disponibles, total)
VALUES 
    ('Don Quijote de la Mancha', 'Miguel de Cervantes', 'Editorial Ejemplo', '1605', '9788424922580', 'Novela', 
     'La historia del ingenioso hidalgo Don Quijote de la Mancha y sus aventuras.', 2, 2),
    ('Cien años de soledad', 'Gabriel García Márquez', 'Editorial Ejemplo', '1967', '9780307474728', 'Novela', 
     'La saga de la familia Buendía y el pueblo de Macondo.', 1, 1),
    ('El principito', 'Antoine de Saint-Exupéry', 'Editorial Ejemplo', '1943', '9788498381498', 'Infantil', 
     'Un pequeño príncipe viaja por diferentes planetas y aprende sobre la vida.', 3, 3);