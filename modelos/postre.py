class Postre:

    def __init__(self, id_receta, nombre, precio, imagen):
        self.id_postre = None
        self.id_receta = id_receta
        self.nombre = nombre
        self.precio = precio
        self.imagen = imagen

    def __str__(self):
        return (
            f"[{self.id_postre}] "
            f"{self.nombre} | "
            f"S/ {self.precio:.2f}"
        )