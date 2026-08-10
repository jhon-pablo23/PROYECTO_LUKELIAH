class Usuario:
    def __init__(self, nombre, correo, contrasena, id_usuario=None):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena

    def to_dict(self):
        # Nunca se devuelve la contraseña al cliente
        return {"id_usuario": self.id_usuario, "nombre": self.nombre, "correo": self.correo}
