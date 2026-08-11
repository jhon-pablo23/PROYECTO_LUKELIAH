from fastapi import APIRouter, HTTPException

from dao.postre_dao import (
    PostreDAO,
    PostreNoEncontradoError,
)
from modelos.postre import Postre
from schemas.postre_schema import (
    PostreCrear,
    PostreActualizar,
    PostreRespuesta,
)
# ----------------------------------------------------------------------
# ROUTER - Postre
# Define los endpoints HTTP para gestionar los postres disponibles
# en el sistema.
# ----------------------------------------------------------------------
router = APIRouter(
    prefix="/postres",
    tags=["Postres"]
)

dao = PostreDAO()

# GET /postres/
# Lista todos los postres registrados.
@router.get("/", response_model=list[PostreRespuesta])
def listar_postres():
    return dao.obtener_todos()

# GET /postres/{id_postre}
# Busca un postre específico por su ID.
@router.get("/{id_postre}", response_model=PostreRespuesta)
def obtener_postre(id_postre: int):
    postre = dao.buscar_por_id(id_postre)

    if not postre:
        raise HTTPException(
            status_code=404,
            detail=f"Postre ID={id_postre} no encontrado"
        )

    return postre

# POST /postres/
# Registra un nuevo postre.
@router.post(
    "/",
    response_model=PostreRespuesta,
    status_code=201
)
def crear_postre(datos: PostreCrear):
    postre = Postre(
    datos.nombre,
    datos.precio,
    datos.id_receta,
    datos.imagen
)
    
    nuevo = dao.insertar(postre)

    return nuevo.to_dict()

# PUT /postres/{id_postre}
# Actualiza solamente los campos enviados.
@router.put(
    "/{id_postre}",
    response_model=PostreRespuesta
)
def actualizar_postre(
    id_postre: int,
    datos: PostreActualizar
):
    try:
        cambios = datos.model_dump(exclude_none=True)

        postre = dao.actualizar(
            id_postre,
            cambios
        )

        return postre

    except PostreNoEncontradoError as ex:
        raise HTTPException(
            status_code=404,
            detail=str(ex)
        )

# DELETE /postres/{id_postre}
# Elimina un postre si no forma parte del historial de ventas.
@router.delete("/{id_postre}")
def eliminar_postre(id_postre: int):
    try:
        dao.eliminar(id_postre)

        return {
            "mensaje": f"Postre ID={id_postre} eliminado correctamente"
        }

    except PostreNoEncontradoError as ex:
        raise HTTPException(
            status_code=404,
            detail=str(ex)
        )