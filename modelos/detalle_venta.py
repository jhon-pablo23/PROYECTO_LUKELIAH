class DetalleVenta:
    def __init__(self, id_venta, id_postre, cantidad, id_detalle=None):
        self.id_detalle = id_detalle
        self.id_venta = id_venta
        self.id_postre = id_postre
        self.cantidad = cantidad 
    def to_dict(self):
        return {
            "id_detalle": self.id_detalle,
            "id_venta": self.id_venta,
            "id_postre": self.id_postre,
            "cantidad": self.cantidad,
        }