class Venta:

    def __init__(self, fecha, total):
        self.id_venta = None
        self.fecha = fecha
        self.total = total

    def __str__(self):
        return (
            f"[{self.id_venta}] "
            f"Fecha: {self.fecha} | "
            f"Total: S/ {self.total:.2f}"
        )