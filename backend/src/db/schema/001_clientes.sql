CREATE TABLE clientes(
	cliente_id SERIAL NOT NULL,
	taller_id INT NOT NULL REFERENCES talleres(taller_id),
	nombre VARCHAR(100) NOT NULL,
	apellido VARCHAR(100) NOT NULL,
	telefono VARCHAR(20) NOT NULL,
	correo TEXT UNIQUE
)