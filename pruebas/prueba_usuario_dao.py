from modelos.usuario import Usuario
from dao.usuario_dao import UsuarioDAO


dao = UsuarioDAO()


print("===== INSERTAR =====")

usuario1 = Usuario(
    "Pablo",
    "pablo@correo.com",
    "123456"
)

usuario2 = Usuario(
    "Lucy",
    "lucy@correo.com",
    "654321"
)

dao.insertar(usuario1)
dao.insertar(usuario2)


print("\n===== OBTENER TODOS =====")

for usuario in dao.obtener_todos():
    print(usuario)


print("\n===== BUSCAR POR ID =====")

usuario = dao.buscar_por_id(1)

print(usuario)


print("\n===== ACTUALIZAR =====")

dao.actualizar(
    1,
    nombre="Juan Pablo",
    correo="juan@correo.com"
)

print(dao.buscar_por_id(1))


print("\n===== ELIMINAR =====")

dao.eliminar(2)


print("\n===== USUARIOS RESTANTES =====")

for usuario in dao.obtener_todos():
    print(usuario)