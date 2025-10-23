CREATE TABLE cliente_carro (
    cliente_carro_id SERIAL PRIMARY KEY,
    cliente_id INT NOT NULL REFERENCES clientes(cliente_id),
    carro_id INT NOT NULL REFERENCES carros(carro_id),
    placas VARCHAR(20) NOT NULL,
    color VARCHAR(50) 
);