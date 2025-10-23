-- PIEZA_CARRO (N:N carros-piezas)
CREATE TABLE pieza_carro (
    carro_id INT NOT NULL REFERENCES carros(carro_id),
    pieza_id INT NOT NULL REFERENCES piezas(pieza_id),
    PRIMARY KEY (carro_id, pieza_id)
);
