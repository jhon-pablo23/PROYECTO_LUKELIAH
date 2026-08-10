class RecetaIngrediente:
    def __init__(self, id_receta, id_ingrediente, cantidad):
        self.id_receta = id_receta
        self.id_ingrediente = id_ingrediente
        self.cantidad = cantidad
        
def to_dict(self):
        return {
            "id_receta": self.id_postre,
            "id_ingrediente": self.id_receta,
            "cantidad":self.cantidad,
        }