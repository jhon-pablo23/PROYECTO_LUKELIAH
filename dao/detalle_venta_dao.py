from config.base_datos import obtener_conexion
from modelos.detalle_venta import DetalleVenta

class DetalleVentaDAO:
    def insertar(self, id_venta, id_postre, cantidad):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO detalle_venta (id_venta, id_postre, cantidad) VALUES (%s, %s, %s) RETURNING id_detalle",
            (id_venta, id_postre, cantidad),
        )
        id_detalle = cursor.fetchone()["id_detalle"]
        conn.commit()
        conn.close()
        return id_detalle

    def obtener_por_venta(self, id_venta):
        # Se obtiene el precio actual del postre y se calcula
        # el subtotal de cada línea de venta.
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT dv.id_detalle, dv.id_postre, p.nombre, dv.cantidad, p.precio,
                   (dv.cantidad * p.precio) AS subtotal
            FROM detalle_venta dv
            JOIN postre p ON p.id_postre = dv.id_postre
            WHERE dv.id_venta = %s
        """, (id_venta,))
        filas = cursor.fetchall()
        conn.close()
        return filas

