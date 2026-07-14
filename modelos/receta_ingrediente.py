class RecetaIngrediente:

    def __init__(self, id_receta, id_ingrediente, cantidad):
        self.id_receta = id_receta
        self.id_ingrediente = id_ingrediente
        self.cantidad = cantidad

    def __str__(self):
        return (
            f"Receta: {self.id_receta} | "
            f"Ingrediente: {self.id_ingrediente} | "
            f"Cantidad: {self.cantidad}"
        )