from modelos.postre import Postre


class PostreDAO:

    def __init__(self):
        self.__bd = []
        self.__cid = 1

    def insertar(self, postre):
        postre.id_postre = self.__cid
        self.__cid += 1
        self.__bd.append(postre)
        return postre

    def buscar_por_id(self, id_postre):
        for postre in self.__bd:
            if postre.id_postre == id_postre:
                return postre
        return None

    def obtener_todos(self):
        return sorted(self.__bd, key=lambda postre: postre.nombre)

    def actualizar(self, id_postre, nombre=None, id_receta=None, precio=None, imagen=None):
        postre = self.buscar_por_id(id_postre)

        if postre:

            if nombre:
                postre.nombre = nombre

            if id_receta:
                postre.id_receta = id_receta

            if precio is not None:
                postre.precio = precio

            if imagen is not None:
                postre.imagen = imagen

            return postre

        return None

    def eliminar(self, id_postre):
        postre = self.buscar_por_id(id_postre)

        if postre:
            self.__bd.remove(postre)
            return True

        return False