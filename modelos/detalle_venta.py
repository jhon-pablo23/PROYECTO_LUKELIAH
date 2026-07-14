class DetalleVenta:

    def __init__(self, id_venta, id_postre, cantidad):
        self.id_detalle = None
        self.id_venta = id_venta
        self.id_postre = id_postre
        self.cantidad = cantidad

    def __str__(self):
        return (
            f"[{self.id_detalle}] "
            f"Venta: {self.id_venta} | "
            f"Postre: {self.id_postre} | "
            f"Cantidad: {self.cantidad}"
        )