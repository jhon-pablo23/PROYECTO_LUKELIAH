from modelos.venta import Venta


class VentaDAO:

    def __init__(self):
        self.__bd = []
        self.__cid = 1

    def insertar(self, venta):
        venta.id_venta = self.__cid
        self.__cid += 1
        self.__bd.append(venta)
        return venta

    def buscar_por_id(self, id_venta):
        for venta in self.__bd:
            if venta.id_venta == id_venta:
                return venta
        return None

    def obtener_todos(self):
        return sorted(
            self.__bd,
            key=lambda venta: venta.fecha
        )

    def actualizar(self, id_venta, fecha=None, total=None):
        venta = self.buscar_por_id(id_venta)

        if venta is not None:

            if fecha is not None:
                venta.fecha = fecha

            if total is not None:
                venta.total = total

            return venta

        return None

    def eliminar(self, id_venta):
        venta = self.buscar_por_id(id_venta)

        if venta is not None:
            self.__bd.remove(venta)
            return True

        return False

    def total(self):
        return len(self.__bd)