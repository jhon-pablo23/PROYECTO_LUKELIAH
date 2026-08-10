from config.base_datos import obtener_conexion
from modelos.receta_ingrediente import RecetaIngrediente


class RecetaIngredienteDAO:
    def agregar(self, id_receta, id_ingrediente, cantidad):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO receta_ingrediente (id_receta, id_ingrediente, cantidad) "
            "VALUES (%s, %s, %s) "
            "ON CONFLICT (id_receta, id_ingrediente) DO UPDATE SET cantidad = EXCLUDED.cantidad",
            (id_receta, id_ingrediente, cantidad),
        )
        conn.commit()
        conn.close()

    def obtener_por_receta(self, id_receta):
        conn = obtener_conexion()
        cursor = conn.cursor()
        
    # Se utiliza JOIN para obtener los datos del ingrediente
    # junto con la cantidad definida para la receta.
        cursor.execute("""
            SELECT ri.id_ingrediente, i.nombre, i.unidad_medida, ri.cantidad
            FROM receta_ingrediente ri
            JOIN ingrediente i ON i.id_ingrediente = ri.id_ingrediente
            WHERE ri.id_receta = %s
            ORDER BY i.nombre
        """, (id_receta,))
        filas = cursor.fetchall()
        conn.close()
        return filas

    def eliminar(self, id_receta, id_ingrediente):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM receta_ingrediente WHERE id_receta = %s AND id_ingrediente = %s",
            (id_receta, id_ingrediente),
        )
        conn.commit()
        conn.close()

    def eliminar_por_receta(self, id_receta):
        # Se llama ANTES de borrar una receta completa: tu tabla no tiene
        # ON DELETE CASCADE, así que si no se hace esto a mano, el DELETE
        # de la receta falla por la llave foránea.
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM receta_ingrediente WHERE id_receta = %s", (id_receta,))
        conn.commit()
        conn.close()
