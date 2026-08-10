from config.base_datos import obtener_conexion
from modelos.ingrediente import Ingrediente

class IngredienteNoEncontradoError(Exception):
    def __init__(self, id_ingrediente):
        super().__init__(f"Ingrediente ID={id_ingrediente} no encontrado")


class IngredienteDAO:
    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ingrediente ORDER BY id_ingrediente")
        filas = cursor.fetchall()
        conn.close()
        return filas

    def buscar_por_id(self, id_ingrediente):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ingrediente WHERE id_ingrediente = %s", (id_ingrediente,))
        fila = cursor.fetchone()
        conn.close()
        return fila

    def insertar(self, ingrediente):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO ingrediente (nombre, unidad_medida, stock_actual, stock_minimo, costo) "
            "VALUES (%s, %s, %s, %s, %s) RETURNING id_ingrediente",
            (ingrediente.nombre, ingrediente.unidad_medida, ingrediente.stock_actual,
            ingrediente.stock_minimo, ingrediente.costo),
        )
        ingrediente.id_ingrediente = cursor.fetchone()["id_ingrediente"]
        conn.commit()
        conn.close()
        return ingrediente

    def actualizar(self, id_ingrediente, cambios: dict):
        actual = self.buscar_por_id(id_ingrediente)
        if not actual:
            raise IngredienteNoEncontradoError(id_ingrediente)
        datos = {**actual, **cambios}
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE ingrediente SET nombre = %s, unidad_medida = %s, "
            "stock_actual = %s, stock_minimo = %s, costo = %s "
            "WHERE id_ingrediente = %s RETURNING *",
            (datos["nombre"], datos["unidad_medida"], datos["stock_actual"],
            datos["stock_minimo"], datos["costo"], id_ingrediente),
        )
        fila = cursor.fetchone()
        conn.commit()
        conn.close()
        return fila

    def eliminar(self, id_ingrediente):
        if not self.buscar_por_id(id_ingrediente):
            raise IngredienteNoEncontradoError(id_ingrediente)
        conn = obtener_conexion()
        cursor = conn.cursor()
        # OJO: si este ingrediente ya está usado en receta_ingrediente, esto va a fallar
        # por la llave foránea (no tiene ON DELETE CASCADE). Es correcto que falle:
        # no deberías poder borrar un ingrediente que una receta todavía usa.
        cursor.execute("DELETE FROM ingrediente WHERE id_ingrediente = %s", (id_ingrediente,))
        conn.commit()
        conn.close()
