CREATE TYPE estado_enum AS ENUM ('pendiente', 'en_proceso', 'completado');

CREATE TABLE trabajos (
    trabajo_id SERIAL PRIMARY KEY,
    fecha_inicio TIMESTAMP NOT NULL DEFAULT NOW(),
    fecha_final TIMESTAMP,
	cliente_carro_id INT NOT NULL REFERENCES cliente_carro(cliente_carro_id),
	taller_id INT NOT NULL REFERENCES talleres(taller_id),
    facturo BOOLEAN DEFAULT FALSE,
    garantia VARCHAR(100),
    descripcion TEXT,
	estado estado_enum NOT NULL

);