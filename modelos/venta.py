class Venta:
    def __init__(self, fecha=None, total=0, id_venta=None):
        self.id_venta = id_venta
        self.fecha = fecha
        self.total = total

    def to_dict(self):
        return {
            "id_venta": self.id_venta,
            "fecha": self.fecha,
            "total": self.total,
        }
