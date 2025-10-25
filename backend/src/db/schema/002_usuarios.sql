CREATE TYPE rol_enum AS ENUM ('admin', 'gerente', 'trabajador');

CREATE TABLE usuarios (
    usuario_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    rol rol_enum NOT NULL,
    acronimo VARCHAR(50) NOT NULL
);