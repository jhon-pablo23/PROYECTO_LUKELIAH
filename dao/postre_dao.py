from config.base_datos import obtener_conexion
from modelos.postre import Postre

class PostreNoEncontradoError(Exception):
    def __init__(self, id_postre):
        super().__init__(f"Postre ID={id_postre} no encontrado")


class PostreDAO:
    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM postre ORDER BY id_postre")
        filas = cursor.fetchall()
        conn.close()
        return filas

    def buscar_por_id(self, id_postre):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM postre WHERE id_postre = %s", (id_postre,))
        fila = cursor.fetchone()
        conn.close()
        return fila

    def insertar(self, postre):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO postre (id_receta, nombre, precio, imagen) VALUES (%s, %s, %s, %s) RETURNING id_postre",
            (postre.id_receta, postre.nombre, postre.precio, postre.imagen),
        )
        postre.id_postre = cursor.fetchone()["id_postre"]
        conn.commit()
        conn.close()
        return postre

    def actualizar(self, id_postre, cambios: dict):
        actual = self.buscar_por_id(id_postre)
        if not actual:
            raise PostreNoEncontradoError(id_postre)
        datos = {**actual, **cambios}
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE postre SET nombre = %s, precio = %s, id_receta = %s, imagen = %s "
            "WHERE id_postre = %s RETURNING *",
            (datos["nombre"], datos["precio"], datos["id_receta"], datos["imagen"], id_postre),
        )
        fila = cursor.fetchone()
        conn.commit()
        conn.close()
        return fila

    def eliminar(self, id_postre):
        if not self.buscar_por_id(id_postre):
            raise PostreNoEncontradoError(id_postre)
        conn = obtener_conexion()
        cursor = conn.cursor()
        # OJO: si este postre ya aparece en detalle_venta (ya se vendió alguna vez),
        # esto falla por la FK (no tiene ON DELETE CASCADE) — correcto: no se debe
        # poder borrar un postre que forma parte del historial de ventas.
        cursor.execute("DELETE FROM postre WHERE id_postre = %s", (id_postre,))
        conn.commit()
        conn.close()
