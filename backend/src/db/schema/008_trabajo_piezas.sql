-- TRABAJO_PIEZAS (N:N trabajos-piezas)
CREATE TABLE trabajo_piezas (
    trabajo_id INT NOT NULL REFERENCES trabajos(trabajo_id),
    pieza_id INT NOT NULL REFERENCES piezas(pieza_id),
    cantidad_usada INT DEFAULT 1,
    PRIMARY KEY (trabajo_id, pieza_id)
);