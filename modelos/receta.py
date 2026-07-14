class Receta:

    def __init__(self, nombre, porciones, procedimiento):
        self.id_receta = None
        self.nombre = nombre
        self.porciones = porciones
        self.procedimiento = procedimiento

    def __str__(self):
        return (
            f"[{self.id_receta}] "
            f"{self.nombre} | "
            f"Porciones: {self.porciones}"
        )