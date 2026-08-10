from datetime import date
from config.base_datos import obtener_conexion
from dao.detalle_venta_dao import DetalleVentaDAO
from modelos.venta import Venta



class VentaDAO:
    """
    Gestiona las ventas y sus detalles.
    Las ventas se conservan como historial y no se permite
    su eliminación.
    """
    def __init__(self):
        self.__detalle_dao = DetalleVentaDAO()

    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM venta ORDER BY id_venta DESC")
        ventas = cursor.fetchall()
        conn.close()
        for v in ventas:
            v["detalle"] = self.__detalle_dao.obtener_por_venta(v["id_venta"])
        return ventas

    def buscar_por_id(self, id_venta):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM venta WHERE id_venta = %s", (id_venta,))
        venta = cursor.fetchone()
        conn.close()
        if venta:
            venta["detalle"] = self.__detalle_dao.obtener_por_venta(id_venta)
        return venta

    def registrar(self, lineas):
        """
        lineas: [{ "id_postre": int, "cantidad": int }, ...]
        El total se calcula aquí con el precio real de cada postre, nunca
        confiando en un total que venga del frontend. La fecha se guarda como
        texto (DD/MM/AAAA) porque así está definida tu columna venta.fecha.
        """
        conn = obtener_conexion()
        cursor = conn.cursor()

        total = 0
        for linea in lineas:
            cursor.execute("SELECT precio FROM postre WHERE id_postre = %s", (linea["id_postre"],))
            fila = cursor.fetchone()
            if not fila:
                conn.close()
                raise ValueError(f"Postre ID={linea['id_postre']} no encontrado")
            total += float(fila["precio"]) * linea["cantidad"]

        fecha_texto = date.today().strftime("%d/%m/%Y")
        cursor.execute(
            "INSERT INTO venta (fecha, total) VALUES (%s, %s) RETURNING id_venta",
            (fecha_texto, total),
        )
        id_venta = cursor.fetchone()["id_venta"]

        for linea in lineas:
            cursor.execute(
                "INSERT INTO detalle_venta (id_venta, id_postre, cantidad) VALUES (%s, %s, %s)",
                (id_venta, linea["id_postre"], linea["cantidad"]),
            )

        conn.commit()
        conn.close()
        return self.buscar_por_id(id_venta)


    def obtener_resumen(self, fecha_inicio, fecha_fin):
        """
        Para el módulo Reportes. IMPORTANTE: venta.fecha es TEXT en formato
        DD/MM/AAAA, así que se convierte con TO_DATE() antes de comparar
        con el rango — un BETWEEN directo sobre texto daría resultados mal
        ordenados (compararía como si fueran palabras, no fechas).
        """
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) AS cantidad_ventas, COALESCE(SUM(total), 0) AS total_recaudado
            FROM venta
            WHERE TO_DATE(fecha, 'DD/MM/YYYY') BETWEEN %s AND %s
        """, (fecha_inicio, fecha_fin))
        resumen = cursor.fetchone()

        cursor.execute("""
            SELECT id_venta, fecha, total
            FROM venta
            WHERE TO_DATE(fecha, 'DD/MM/YYYY') BETWEEN %s AND %s
            ORDER BY TO_DATE(fecha, 'DD/MM/YYYY') DESC
        """, (fecha_inicio, fecha_fin))
        resumen["ventas"] = cursor.fetchall()
        conn.close()
        return resumen
