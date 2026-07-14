from dao.postre_dao import PostreDAO
from modelos.postre import Postre


dao = PostreDAO()

print("===== INSERTAR =====")

postre1 = Postre(
    1,
    "Torta de Chocolate",
    65.00,
    "torta.jpg"
)

postre2 = Postre(
    2,
    "Cheesecake",
    55.00,
    "cheesecake.jpg"
)
dao.insertar(postre1)
dao.insertar(postre2)

for postre in dao.obtener_todos():
    print(postre)


print("\n===== BUSCAR POR ID =====")

print(dao.buscar_por_id(1))


print("\n===== ACTUALIZAR =====")

dao.actualizar(2, precio=60.00)

for postre in dao.obtener_todos():
    print(postre)


print("\n===== ELIMINAR =====")

dao.eliminar(1)

for postre in dao.obtener_todos():
    print(postre)

"""3. Ejecuta el archivo

Escribe exactamente:

python -m pruebas.prueba_postre_dao

y presiona Enter. """