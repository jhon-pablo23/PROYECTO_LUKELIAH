class Ingrediente:
    def __init__(self, nombre, unidad_medida, stock_actual, stock_minimo, costo, id_ingrediente=None):
        self.id_ingrediente = id_ingrediente
        self.nombre = nombre
        self.unidad_medida = unidad_medida
        self.stock_actual = stock_actual
        self.stock_minimo = stock_minimo
        self.costo = costo

    def to_dict(self):
        return {
            "id_ingrediente": self.id_ingrediente,
            "nombre": self.nombre,
            "unidad_medida": self.unidad_medida,
            "stock_actual": self.stock_actual,
            "stock_minimo": self.stock_minimo,
            "costo": self.costo,
        }
