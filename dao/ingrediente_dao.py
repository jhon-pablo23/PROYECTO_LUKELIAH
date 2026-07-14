from modelos.ingrediente import Ingrediente


class IngredienteDAO:

    def __init__(self):
        self.__bd = []
        self.__cid = 1

    def insertar(self, ingrediente):
        ingrediente.id_ingrediente = self.__cid
        self.__cid += 1
        self.__bd.append(ingrediente)
        return ingrediente

    def buscar_por_id(self, id_ingrediente):
        for ingrediente in self.__bd:
            if ingrediente.id_ingrediente == id_ingrediente:
                return ingrediente

        return None

    def obtener_todos(self):
        return self.__bd

    def actualizar(
        self,
        id_ingrediente,
        nombre=None,
        unidad_medida=None,
        stock_actual=None,
        stock_minimo=None,
        costo=None,
    ):
        ingrediente = self.buscar_por_id(id_ingrediente)

        if ingrediente:

            if nombre:
                ingrediente.nombre = nombre

            if unidad_medida:
                ingrediente.unidad_medida = unidad_medida

            if stock_actual is not None:
                ingrediente.stock_actual = stock_actual

            if stock_minimo is not None:
                ingrediente.stock_minimo = stock_minimo

            if costo is not None:
                ingrediente.costo = costo

            return ingrediente

        return None

    def eliminar(self, id_ingrediente):
        ingrediente = self.buscar_por_id(id_ingrediente)

        if ingrediente:
            self.__bd.remove(ingrediente)
            return True

        return False