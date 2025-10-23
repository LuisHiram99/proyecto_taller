-- TRABAJO_USUARIOS (N:N trabajos-usuarios)
CREATE TABLE trabajo_usuarios (
    trabajo_id INT NOT NULL REFERENCES trabajos(trabajo_id),
    usuario_id INT NOT NULL REFERENCES usuarios(usuario_id),
    rol_en_trabajo VARCHAR(50),
    PRIMARY KEY (trabajo_id, usuario_id)
);
