from fastapi import APIRouter, HTTPException

from dao.usuario_dao import UsuarioDAO, CorreoDuplicadoError
from modelos.usuario import Usuario
from schemas.usuario_schema import (
    UsuarioCrear,
    UsuarioActualizar,
    UsuarioRespuesta,
    UsuarioLogin,
)
# ----------------------------------------------------------------------
# ROUTER - Usuario
# Define los endpoints HTTP para gestionar los usuarios del sistema.
# El router recibe los datos validados por los schemas y utiliza
# UsuarioDAO para realizar las operaciones en PostgreSQL.
# ----------------------------------------------------------------------
router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)
dao = UsuarioDAO()

# ----------------------------------------------------------------------
# GET /usuarios/
# Lista todos los usuarios registrados.
# La contraseña no se devuelve en la respuesta.
# ----------------------------------------------------------------------
@router.get("/", response_model=list[UsuarioRespuesta])
def listar_usuarios():
    return dao.obtener_todos()

# ----------------------------------------------------------------------
# POST /usuarios/login
# Verifica el correo y contraseña enviados por el usuario.
# ----------------------------------------------------------------------

@router.post("/login", response_model=UsuarioRespuesta)
def login(datos: UsuarioLogin):

    usuario = dao.verificar_credenciales(
        datos.correo,
        datos.contrasena
    )

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="Correo o contraseña incorrectos"
        )

    return usuario

# ----------------------------------------------------------------------
# GET /usuarios/{id_usuario}
# Busca un usuario específico por su ID.
# ----------------------------------------------------------------------
@router.get("/{id_usuario}", response_model=UsuarioRespuesta)
def obtener_usuario(id_usuario: int):

    usuario = dao.buscar_por_id(id_usuario)

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail=f"Usuario ID={id_usuario} no encontrado"
        )

    return usuario
# ----------------------------------------------------------------------
# POST /usuarios/
# Registra un nuevo usuario.
# ----------------------------------------------------------------------
@router.post(
    "/",
    response_model=UsuarioRespuesta,
    status_code=201
)
def crear_usuario(datos: UsuarioCrear):

    try:
        usuario = Usuario(
            datos.nombre,
            datos.correo,
            datos.contrasena
        )

        nuevo = dao.insertar(usuario)

        # insertar() devuelve un objeto Usuario.
        return nuevo.to_dict()

    except CorreoDuplicadoError as ex:
        raise HTTPException(
            status_code=400,
            detail=str(ex)
        )
# ----------------------------------------------------------------------
# PUT /usuarios/{id_usuario}
# Actualiza los datos de un usuario.
# Los campos que no se envían conservan su valor actual.
# ----------------------------------------------------------------------
@router.put(
    "/{id_usuario}",
    response_model=UsuarioRespuesta
)
def actualizar_usuario(
    id_usuario: int,
    datos: UsuarioActualizar
):

    usuario = dao.actualizar(
        id_usuario,
        datos.nombre,
        datos.correo,
        datos.contrasena
    )

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail=f"Usuario ID={id_usuario} no encontrado"
        )

    return usuario

# ----------------------------------------------------------------------
# DELETE /usuarios/{id_usuario}
# Elimina un usuario registrado.
# ----------------------------------------------------------------------

@router.delete("/{id_usuario}")
def eliminar_usuario(id_usuario: int):

    usuario = dao.buscar_por_id(id_usuario)

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail=f"Usuario ID={id_usuario} no encontrado"
        )

    dao.eliminar(id_usuario)

    return {
        "mensaje": f"Usuario ID={id_usuario} eliminado correctamente"
    }