from dao.venta_dao import VentaDAO
from modelos.venta import Venta


dao = VentaDAO()

print("===== INSERTAR =====")

v1 = dao.insertar(
    Venta(
        "2026-07-13",
        120.00
    )
)

v2 = dao.insertar(
    Venta(
        "2026-07-14",
        85.50
    )
)

for venta in dao.obtener_todos():
    print(venta)

print()

print("===== BUSCAR POR ID =====")

venta = dao.buscar_por_id(1)

if venta:
    print(venta)

print()

print("===== ACTUALIZAR =====")

dao.actualizar(
    1,
    total=150.00
)

print(dao.buscar_por_id(1))

print()

print("===== ELIMINAR =====")

dao.eliminar(2)

for venta in dao.obtener_todos():
    print(venta)

print()

print("===== TOTAL =====")

print(dao.total())

"""# Comando para ejecutar

Desde la raíz del proyecto (`D:\PROYECTO_LUKELIAH`):

```bash
python -m pruebas.prueba_venta_dao"""