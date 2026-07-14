class Ingrediente:

    def __init__(self, nombre, unidad_medida, stock_actual, stock_minimo, costo):
        self.id_ingrediente = None
        self.nombre = nombre
        self.unidad_medida = unidad_medida
        self.stock_actual = stock_actual
        self.stock_minimo = stock_minimo
        self.costo = costo

    def __str__(self):
        return (
            f"[{self.id_ingrediente}] "
            f"{self.nombre} | "
            f"{self.stock_actual} {self.unidad_medida} | "
            f"S/ {self.costo:.2f}"
        )