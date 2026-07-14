class Usuario:

    def __init__(self, nombre, correo, contrasena):
        self.id_usuario = None
        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena

    def __str__(self):
        return (
            f"[{self.id_usuario}] "
            f"{self.nombre} | "
            f"{self.correo}"
        )