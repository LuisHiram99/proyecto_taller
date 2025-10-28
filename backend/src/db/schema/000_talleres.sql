CREATE TABLE talleres (
	taller_id SERIAL PRIMARY KEY,
	nombre_taller VARCHAR(100) NOT NULL,
	direccion VARCHAR(100),
	horario_apertura TIMESTAMP,
	horario_cierre TIMESTAMP
)