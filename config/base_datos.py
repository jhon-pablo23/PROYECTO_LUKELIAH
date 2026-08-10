import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()


# ----------------------------------------------------------------------
# CONEXIÓN A POSTGRESQL
# ----------------------------------------------------------------------

def obtener_conexion():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "lukeliah_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
    )

    # Devuelve cada fila como diccionario.
    conn.cursor_factory = RealDictCursor

    return conn


# ----------------------------------------------------------------------
# INICIALIZACIÓN DE TABLAS
#
# Crea las tablas solamente si todavía no existen.
# No elimina datos existentes.
# ----------------------------------------------------------------------

def inicializar():
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuario (
            id_usuario SERIAL PRIMARY KEY,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL UNIQUE,
            contrasena TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingrediente (
            id_ingrediente SERIAL PRIMARY KEY,
            nombre TEXT NOT NULL,
            unidad_medida TEXT NOT NULL,
            stock_actual NUMERIC(10,2) NOT NULL,
            stock_minimo NUMERIC(10,2) NOT NULL,
            costo NUMERIC(10,2) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS receta (
            id_receta SERIAL PRIMARY KEY,
            nombre TEXT NOT NULL,
            porciones INTEGER NOT NULL,
            procedimiento TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS receta_ingrediente (
            id_receta INTEGER NOT NULL,
            id_ingrediente INTEGER NOT NULL,
            cantidad NUMERIC(10,2) NOT NULL,

            PRIMARY KEY (id_receta, id_ingrediente),

            FOREIGN KEY (id_receta)
                REFERENCES receta(id_receta),

            FOREIGN KEY (id_ingrediente)
                REFERENCES ingrediente(id_ingrediente)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS postre (
            id_postre SERIAL PRIMARY KEY,
            id_receta INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            precio NUMERIC(10,2) NOT NULL,
            imagen TEXT,

            FOREIGN KEY (id_receta)
                REFERENCES receta(id_receta)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS venta (
            id_venta SERIAL PRIMARY KEY,
            fecha TEXT NOT NULL,
            total NUMERIC(10,2) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detalle_venta (
            id_detalle SERIAL PRIMARY KEY,
            id_venta INTEGER NOT NULL,
            id_postre INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,

            FOREIGN KEY (id_venta)
                REFERENCES venta(id_venta),

            FOREIGN KEY (id_postre)
                REFERENCES postre(id_postre)
        )
    """)

    conn.commit()
    conn.close()