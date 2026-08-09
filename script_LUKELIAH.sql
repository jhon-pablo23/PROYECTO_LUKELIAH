-- =================
-- SCRIPT: LUKELIAH
-- Base de datos: lukeliah_db
-- Motor: PostgreSQL
-- =================
-- Eliminar tablas si ya existen (orden importante por FK)
DROP TABLE IF EXISTS detalle_venta;
DROP TABLE IF EXISTS venta;
DROP TABLE IF EXISTS postre;
DROP TABLE IF EXISTS receta_ingrediente;
DROP TABLE IF EXISTS receta;
DROP TABLE IF EXISTS ingrediente;
DROP TABLE IF EXISTS usuario;

CREATE TABLE usuario (
    id_usuario SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    correo TEXT NOT NULL UNIQUE,
    contrasena TEXT NOT NULL
);

CREATE TABLE ingrediente (
    id_ingrediente SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    unidad_medida TEXT NOT NULL,
    stock_actual NUMERIC(10,2) NOT NULL,
    stock_minimo NUMERIC(10,2) NOT NULL,
    costo NUMERIC(10,2) NOT NULL
);

CREATE TABLE receta (
    id_receta SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    porciones INTEGER NOT NULL,
    procedimiento TEXT NOT NULL
);

CREATE TABLE receta_ingrediente (
    id_receta INTEGER NOT NULL,
    id_ingrediente INTEGER NOT NULL,
    cantidad NUMERIC(10,2) NOT NULL,
    PRIMARY KEY (id_receta,id_ingrediente),
    FOREIGN KEY (id_receta) REFERENCES receta(id_receta),
    FOREIGN KEY (id_ingrediente) REFERENCES ingrediente(id_ingrediente)
);

CREATE TABLE postre (
    id_postre SERIAL PRIMARY KEY,
    id_receta INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    precio NUMERIC(10,2) NOT NULL,
    imagen TEXT,
    FOREIGN KEY (id_receta) REFERENCES receta(id_receta)
);

CREATE TABLE venta (
    id_venta SERIAL PRIMARY KEY,
    fecha TEXT NOT NULL,
    total NUMERIC(10,2) NOT NULL
);

CREATE TABLE detalle_venta (
    id_detalle SERIAL PRIMARY KEY,
    id_venta INTEGER NOT NULL,
    id_postre INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    FOREIGN KEY (id_venta) REFERENCES venta(id_venta),
    FOREIGN KEY (id_postre) REFERENCES postre(id_postre)
);

-- DATOS DE PRUEBA

INSERT INTO usuario (nombre,correo,contrasena) VALUES
('Administrador','admin@lukeliah.com','admin123');

INSERT INTO ingrediente (nombre,unidad_medida,stock_actual,stock_minimo,costo) VALUES
('Harina','kg',10,2,3.50),
('Azucar','kg',8,2,4.00),
('Chocolate','kg',5,1,18.00);

INSERT INTO receta (nombre,porciones,procedimiento) VALUES
('Torta de Chocolate',12,'Mezclar ingredientes y hornear.');

INSERT INTO receta_ingrediente (id_receta,id_ingrediente,cantidad) VALUES
(1,1,1.00),
(1,2,0.50),
(1,3,0.80);

INSERT INTO postre (id_receta,nombre,precio,imagen) VALUES
(1,'Torta de Chocolate',65.00,'torta_chocolate.jpg');

INSERT INTO venta (fecha,total) VALUES
('2026-07-31 10:00:00',130.00);

INSERT INTO detalle_venta (id_venta,id_postre,cantidad) VALUES
(1,1,2);

-- VERIFICACION

SELECT 'usuario' AS tabla, COUNT(*) AS registros FROM usuario
UNION ALL
SELECT 'ingrediente', COUNT(*) FROM ingrediente
UNION ALL
SELECT 'receta', COUNT(*) FROM receta
UNION ALL
SELECT 'receta_ingrediente', COUNT(*) FROM receta_ingrediente
UNION ALL
SELECT 'postre', COUNT(*) FROM postre
UNION ALL
SELECT 'venta', COUNT(*) FROM venta
UNION ALL
SELECT 'detalle_venta', COUNT(*) FROM detalle_venta;