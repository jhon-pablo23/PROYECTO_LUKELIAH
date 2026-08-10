class Receta:
    def __init__(self, nombre, porciones, procedimiento, id_receta=None):
        self.id_receta = id_receta
        self.nombre = nombre
        self.porciones = porciones
        self.procedimiento = procedimiento

    def to_dict(self):
        return {
            "id_receta": self.id_receta,
            "nombre": self.nombre,
            "porciones": self.porciones,
            "procedimiento": self.procedimiento,
        }
