from modelos.detalle_venta import DetalleVenta


class DetalleVentaDAO:

    def __init__(self):
        self.__bd = []
        self.__cid = 1

    def insertar(self, detalle):
        detalle.id_detalle = self.__cid
        self.__cid += 1
        self.__bd.append(detalle)
        return detalle

    def buscar_por_id(self, id_detalle):
        for detalle in self.__bd:
            if detalle.id_detalle == id_detalle:
                return detalle
        return None

    def obtener_todos(self):
        return sorted(
            self.__bd,
            key=lambda detalle: detalle.id_detalle
        )

    def actualizar(
        self,
        id_detalle,
        id_venta=None,
        id_postre=None,
        cantidad=None
    ):
        detalle = self.buscar_por_id(id_detalle)

        if detalle:

            if id_venta is not None:
                detalle.id_venta = id_venta

            if id_postre is not None:
                detalle.id_postre = id_postre

            if cantidad is not None:
                detalle.cantidad = cantidad

            return True

        return False

    def eliminar(self, id_detalle):
        detalle = self.buscar_por_id(id_detalle)

        if detalle:
            self.__bd.remove(detalle)
            return True

        return False

    def total(self):
        return len(self.__bd)