from modelos.receta import Receta


class RecetaDAO:

    def __init__(self):
        self.__bd = []
        self.__cid = 1

    def insertar(self, receta):
        receta.id_receta = self.__cid
        self.__cid += 1
        self.__bd.append(receta)
        return receta

    def buscar_por_id(self, id_receta):
        for receta in self.__bd:
            if receta.id_receta == id_receta:
                return receta
        return None

    def obtener_todos(self):
        return self.__bd

    def actualizar(
        self,
        id_receta,
        nombre=None,
        porciones=None,
        procedimiento=None
    ):
        receta = self.buscar_por_id(id_receta)

        if receta:

            if nombre is not None:
                receta.nombre = nombre

            if porciones is not None:
                receta.porciones = porciones

            if procedimiento is not None:
                receta.procedimiento = procedimiento

            return receta

        return None

    def eliminar(self, id_receta):
        receta = self.buscar_por_id(id_receta)

        if receta:
            self.__bd.remove(receta)
            return True

        return False