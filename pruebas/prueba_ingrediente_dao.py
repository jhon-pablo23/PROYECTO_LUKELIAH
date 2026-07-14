from dao.ingrediente_dao import IngredienteDAO
from modelos.ingrediente import Ingrediente


dao = IngredienteDAO()

print("===== INSERTAR =====")

ingrediente1 = Ingrediente(
    "Harina",
    "kg",
    20,
    5,
    3.50
)

ingrediente2 = Ingrediente(
    "Azucar",
    "kg",
    15,
    3,
    4.20
)

dao.insertar(ingrediente1)
dao.insertar(ingrediente2)

for ingrediente in dao.obtener_todos():
    print(ingrediente)

print()

print("===== BUSCAR POR ID =====")

ingrediente = dao.buscar_por_id(1)

if ingrediente:
    print(ingrediente)
else:
    print("Ingrediente no encontrado")

print()

print("===== ACTUALIZAR =====")

dao.actualizar(
    1,
    stock_actual=30,
    costo=3.80
)

ingrediente = dao.buscar_por_id(1)

if ingrediente:
    print(ingrediente)

print()

print("===== ELIMINAR =====")

resultado = dao.eliminar(2)

print(resultado)

print()

print("===== LISTA FINAL =====")

for ingrediente in dao.obtener_todos():
    print(ingrediente)


"""Cómo ejecutarlo

Desde la carpeta principal del proyecto:

python -m pruebas.prueba_ingrediente_dao"""