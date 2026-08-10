from config.base_datos import obtener_conexion
from dao.receta_ingrediente_dao import RecetaIngredienteDAO
from modelos.receta import Receta

class RecetaNoEncontradaError(Exception):
    def __init__(self, id_receta):
        super().__init__(f"Receta ID={id_receta} no encontrada")


class RecetaDAO:
    def __init__(self):
        self.__ri_dao = RecetaIngredienteDAO()

    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM receta ORDER BY id_receta")
        filas = cursor.fetchall()
        conn.close()
        return filas

    def buscar_por_id(self, id_receta):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM receta WHERE id_receta = %s", (id_receta,))
        fila = cursor.fetchone()
        conn.close()
        return fila

    def insertar(self, receta):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO receta (nombre, porciones, procedimiento) VALUES (%s, %s, %s) RETURNING id_receta",
            (receta.nombre, receta.porciones, receta.procedimiento),
        )
        receta.id_receta = cursor.fetchone()["id_receta"]
        conn.commit()
        conn.close()
        return receta

    def actualizar(self, id_receta, cambios: dict):
        actual = self.buscar_por_id(id_receta)
        if not actual:
            raise RecetaNoEncontradaError(id_receta)
        datos = {**actual, **cambios}
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE receta SET nombre = %s, porciones = %s, procedimiento = %s "
            "WHERE id_receta = %s RETURNING *",
            (datos["nombre"], datos["porciones"], datos["procedimiento"], id_receta),
        )
        fila = cursor.fetchone()
        conn.commit()
        conn.close()
        return fila

    def eliminar(self, id_receta):
        if not self.buscar_por_id(id_receta):
            raise RecetaNoEncontradaError(id_receta)
        self.__ri_dao.eliminar_por_receta(id_receta)  # limpia receta_ingrediente primero (sin CASCADE)
        conn = obtener_conexion()
        cursor = conn.cursor()
        # OJO: si esta receta ya tiene un postre creado con ella, esto va a fallar
        # por la FK de postre.id_receta (no tiene ON DELETE CASCADE, y así debe ser:
        # no deberías poder borrar la receta de un postre que sigue existiendo).
        cursor.execute("DELETE FROM receta WHERE id_receta = %s", (id_receta,))
        conn.commit()
        conn.close()

    # ---- delega en RecetaIngredienteDAO, mismos nombres que ya usan tus routers ----

    def obtener_ingredientes(self, id_receta):
        return self.__ri_dao.obtener_por_receta(id_receta)

    def agregar_ingrediente(self, id_receta, id_ingrediente, cantidad):
        self.__ri_dao.agregar(id_receta, id_ingrediente, cantidad)

    def quitar_ingrediente(self, id_receta, id_ingrediente):
        self.__ri_dao.eliminar(id_receta, id_ingrediente)
