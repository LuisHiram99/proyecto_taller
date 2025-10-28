

CREATE TABLE pieza_taller(
	taller_id INT NOT NULL REFERENCES talleres(taller_id),
	pieza_id INT NOT NULL REFERENCES piezas(pieza_id),
	cantidad INT NOT NULL DEFAULT 1,
	precio_compra INT,
	precio_venta INT,

	PRIMARY KEY (pieza_id, taller_id)
);