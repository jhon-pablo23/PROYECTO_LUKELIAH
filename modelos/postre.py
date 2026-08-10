class Postre:
    def __init__(self, nombre, precio, id_receta=None, imagen=None, id_postre=None):
        self.id_postre = id_postre
        self.id_receta = id_receta
        self.nombre = nombre
        self.precio = precio
        self.imagen = imagen

    def to_dict(self):
        return {
            "id_postre": self.id_postre,
            "id_receta": self.id_receta,
            "nombre": self.nombre,
            "precio": self.precio,
            "imagen": self.imagen,
        }
