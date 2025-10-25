-- CLIENTES
CREATE TABLE clientes (
    cliente_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    correo VARCHAR(100)
);

-- USUARIOS
CREATE TABLE usuarios (
    usuario_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    rol VARCHAR(50) NOT NULL,
    acronimo VARCHAR(20)
);

-- CARROS
CREATE TABLE carros (
    carro_id SERIAL PRIMARY KEY,
    año INT NOT NULL,
    modelo VARCHAR(100) NOT NULL
);

-- CLIENTE_CARRO
CREATE TABLE cliente_carro (
    cliente_carro_id SERIAL PRIMARY KEY,
    cliente_id INT NOT NULL REFERENCES clientes(cliente_id),
    carro_id INT NOT NULL REFERENCES carros(carro_id),
    placas VARCHAR(20) NOT NULL,
    color VARCHAR(50)
);

-- PIEZAS
CREATE TABLE piezas (
    pieza_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    cantidad INT NOT NULL,
    precio_compra NUMERIC(10,2),
    precio_venta NUMERIC(10,2)
);

-- PIEZA_CARRO (N:N carros-piezas)
CREATE TABLE pieza_carro (
    carro_id INT NOT NULL REFERENCES carros(carro_id),
    pieza_id INT NOT NULL REFERENCES piezas(pieza_id),
    PRIMARY KEY (carro_id, pieza_id)
);

-- TRABAJOS
CREATE TABLE trabajos (
    trabajo_id SERIAL PRIMARY KEY,
    fecha_inicio TIMESTAMP NOT NULL DEFAULT NOW(),
    fecha_final TIMESTAMP,
    cliente_carro_id INT NOT NULL REFERENCES cliente_carro(cliente_carro_id),
    facturo BOOLEAN DEFAULT FALSE,
    garantia VARCHAR(100),
    descripcion TEXT
);

-- TRABAJO_PIEZAS (N:N trabajos-piezas)
CREATE TABLE trabajo_piezas (
    trabajo_id INT NOT NULL REFERENCES trabajos(trabajo_id),
    pieza_id INT NOT NULL REFERENCES piezas(pieza_id),
    cantidad_usada INT DEFAULT 1,
    PRIMARY KEY (trabajo_id, pieza_id)
);

-- TRABAJO_USUARIOS (N:N trabajos-usuarios)
CREATE TABLE trabajo_usuarios (
    trabajo_id INT NOT NULL REFERENCES trabajos(trabajo_id),
    usuario_id INT NOT NULL REFERENCES usuarios(usuario_id),
    rol_en_trabajo VARCHAR(50),
    PRIMARY KEY (trabajo_id, usuario_id)
);
