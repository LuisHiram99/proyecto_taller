CREATE TYPE rol_enum AS ENUM ('admin', 'gerente', 'trabajador');

CREATE TABLE usuarios(
	usuario_id SERIAL PRIMARY KEY,
	taller_id INT NOT NULL REFERENCES talleres(taller_id),
	nombre VARCHAR(100) NOT NULL,
	apellido VARCHAR(100) NOT NULL,
	telefono VARCHAR(20),
	correo TEXT UNIQUE,
	hashpassword VARCHAR(60) NOT NULL,
	rol rol_enum NOT NULL,
	pseudonimo VARCHAR(50)
);