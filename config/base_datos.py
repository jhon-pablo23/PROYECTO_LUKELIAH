import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()
# CONEXION A POSTGRESQL 
# psycopg2 es el driver (el driver para conectar Python con PostgreSQL).
def obtener_conexion():
    conn=psycopg2.connect(
        
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "lukeliah_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
    )
        
        # RealDictCursor hace que cada fila se devuelva como un diccionario real en Python,
        # a diferencia de Tuples que (que tambien actua como Dict pero no es exactamente uno).
        # Esto permite hacer dict['col'] y retornar las filas directamente a FastAPI.
    conn.cursor_factory = RealDictCursor
    return conn


def inicializar():
    # Crea las tablas si aun no existen - Se debe declarar al iniciar el sistema
    # "IF NOT EXISTS" evita un error si la tabla ya fue creada en una ejecucion anterior
    conn = obtener_conexion()
    cursor = conn.cursor()
    
    # Eliminar tablas si ya existen (orden importante por FK)
    cursor.execute("DROP TABLE IF EXISTS detalle_venta;")
    cursor.execute("DROP TABLE IF EXISTS venta;")
    cursor.execute("DROP TABLE IF EXISTS postre;")
    cursor.execute("DROP TABLE IF EXISTS receta_ingrediente;")
    cursor.execute("DROP TABLE IF EXISTS receta;")
    cursor.execute("DROP TABLE IF EXISTS ingrediente;")
    cursor.execute("DROP TABLE IF EXISTS usuario;")

    # Tablas de Lukeliah
    cursor.execute("""
        CREATE TABLE usuario (
            id_usuario SERIAL PRIMARY KEY,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL UNIQUE,
            contrasena TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE ingrediente (
            id_ingrediente SERIAL PRIMARY KEY,
            nombre TEXT NOT NULL,
            unidad_medida TEXT NOT NULL,
            stock_actual NUMERIC(10,2) NOT NULL,
            stock_minimo NUMERIC(10,2) NOT NULL,
            costo NUMERIC(10,2) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE receta (
            id_receta SERIAL PRIMARY KEY,
            nombre TEXT NOT NULL,
            porciones INTEGER NOT NULL,
            procedimiento TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE receta_ingrediente (
            id_receta INTEGER NOT NULL,
            id_ingrediente INTEGER NOT NULL,
            cantidad NUMERIC(10,2) NOT NULL,
            PRIMARY KEY (id_receta,id_ingrediente),
            FOREIGN KEY (id_receta) REFERENCES receta(id_receta),
            FOREIGN KEY (id_ingrediente) REFERENCES ingrediente(id_ingrediente)
        )
    """)

    cursor.execute("""
        CREATE TABLE postre (
            id_postre SERIAL PRIMARY KEY,
            id_receta INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            precio NUMERIC(10,2) NOT NULL,
            imagen TEXT,
            FOREIGN KEY (id_receta) REFERENCES receta(id_receta)
        )
    """)

    cursor.execute("""
        CREATE TABLE venta (
            id_venta SERIAL PRIMARY KEY,
            fecha TEXT NOT NULL,
            total NUMERIC(10,2) NOT NULL
        )
    """)

    # Tabla con llaves foráneas (FOREIGN KEY) que enlaza con venta y postre
    # FOREIGN KEY garantiza integridad referencial: no se puede registrar un detalle
    # con un id_venta o id_postre que no exista en sus tablas respectivas.
    cursor.execute("""
        CREATE TABLE detalle_venta (
            id_detalle SERIAL PRIMARY KEY,
            id_venta INTEGER NOT NULL,
            id_postre INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            FOREIGN KEY (id_venta) REFERENCES venta(id_venta),
            FOREIGN KEY (id_postre) REFERENCES postre(id_postre)
        )
    """)

    conn.commit() # confirma todos los cambios (escribe o "guarda" en la db)
    conn.close()
