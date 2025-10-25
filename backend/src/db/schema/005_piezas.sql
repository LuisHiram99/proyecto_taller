CREATE TABLE piezas (
    pieza_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    cantidad INT NOT NULL,
    precio_compra NUMERIC(10,2),
    precio_venta NUMERIC(10,2)
);