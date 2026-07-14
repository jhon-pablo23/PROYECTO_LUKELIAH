from dao.receta_dao import RecetaDAO
from modelos.receta import Receta


dao = RecetaDAO()

print("===== INSERTAR =====")

r1 = dao.insertar(
    Receta(
        "Torta de Chocolate",
        12,
        "Mezclar ingredientes y hornear."
    )
)

r2 = dao.insertar(
    Receta(
        "Cheesecake",
        10,
        "Preparar la base, agregar el relleno y refrigerar."
    )
)

for receta in dao.obtener_todos():
    print(receta)

print("\n===== BUSCAR POR ID =====")

print(dao.buscar_por_id(1))

print("\n===== ACTUALIZAR =====")

dao.actualizar(
    2,
    porciones=14,
    procedimiento="Preparar la base, agregar el relleno, refrigerar y decorar."
)

for receta in dao.obtener_todos():
    print(receta)

print("\n===== ELIMINAR =====")

dao.eliminar(1)

for receta in dao.obtener_todos():
    print(receta)