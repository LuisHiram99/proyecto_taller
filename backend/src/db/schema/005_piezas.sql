CREATE TABLE piezas (
    pieza_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
	marca varchar(50) NOT NULL,
	categoria VARCHAR(100) NOT NULL,
	descripcion TEXT
);