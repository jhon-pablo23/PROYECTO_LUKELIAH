from dao.detalle_venta_dao import DetalleVentaDAO
from modelos.detalle_venta import DetalleVenta


dao = DetalleVentaDAO()

print("===== INSERTAR =====")

detalle1 = DetalleVenta(1, 1, 2)
detalle2 = DetalleVenta(1, 2, 3)

dao.insertar(detalle1)
dao.insertar(detalle2)

for detalle in dao.obtener_todos():
    print(detalle)

print("\n===== BUSCAR POR ID =====")

detalle = dao.buscar_por_id(1)

if detalle:
    print(detalle)

print("\n===== ACTUALIZAR =====")

dao.actualizar(
    1,
    cantidad=5
)

for detalle in dao.obtener_todos():
    print(detalle)

print("\n===== ELIMINAR =====")

dao.eliminar(2)

for detalle in dao.obtener_todos():
    print(detalle)

print("\n===== TOTAL =====")

print(dao.total())

"""Cómo ejecutar la prueba

Desde la raíz del proyecto (D:\PROYECTO_LUKELIAH), ejecuta el siguiente comando:

python -m pruebas.prueba_detalle_venta_dao"""