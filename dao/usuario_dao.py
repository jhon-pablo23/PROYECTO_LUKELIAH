class UsuarioDAO:

    def __init__(self):
        self.__bd = []
        self.__cid = 1

    def insertar(self, usuario):
        usuario.id_usuario = self.__cid
        self.__cid += 1
        self.__bd.append(usuario)
        return usuario

    def buscar_por_id(self, id_usuario):
        for usuario in self.__bd:
            if usuario.id_usuario == id_usuario:
                return usuario
        return None

    def obtener_todos(self):
        return self.__bd
    
    def actualizar(
        self,
        id_usuario,
        nombre=None,
        correo=None,
        contrasena=None,
    ):
        usuario = self.buscar_por_id(id_usuario)

        if usuario:

            if nombre:
                usuario.nombre = nombre

            if correo:
                usuario.correo = correo

            if contrasena:
                usuario.contrasena = contrasena

            return usuario

        return None
    
    def eliminar(self, id_usuario):
        usuario = self.buscar_por_id(id_usuario)

        if usuario:
            self.__bd.remove(usuario)
            return True

        return False