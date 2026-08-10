from fastapi import APIRouter, HTTPException

from dao.receta_dao import RecetaDAO, RecetaNoEncontradaError
from modelos.receta import Receta
from schemas.receta_schema import (
    RecetaCrear,
    RecetaActualizar,
    RecetaRespuesta,
)
from schemas.receta_ingrediente_schema import (
    RecetaIngredienteCrear,
    RecetaIngredienteRespuesta,
)


# ----------------------------------------------------------------------
# ROUTER - Receta
#
# Define los endpoints HTTP para gestionar recetas y los ingredientes
# asociados a cada receta.
# ----------------------------------------------------------------------

router = APIRouter(
    prefix="/recetas",
    tags=["Recetas"]
)

dao = RecetaDAO()


# GET /recetas/
# Lista todas las recetas registradas.
@router.get("/", response_model=list[RecetaRespuesta])
def listar_recetas():
    return dao.obtener_todos()


# GET /recetas/{id_receta}
# Busca una receta específica por su ID.
@router.get("/{id_receta}", response_model=RecetaRespuesta)
def obtener_receta(id_receta: int):
    receta = dao.buscar_por_id(id_receta)

    if not receta:
        raise HTTPException(
            status_code=404,
            detail=f"Receta ID={id_receta} no encontrada"
        )

    return receta


# POST /recetas/
# Registra una nueva receta.
@router.post(
    "/",
    response_model=RecetaRespuesta,
    status_code=201
)
def crear_receta(datos: RecetaCrear):

    receta = Receta(
        datos.nombre,
        datos.porciones,
        datos.procedimiento
    )

    nueva = dao.insertar(receta)

    return nueva.to_dict()


# PUT /recetas/{id_receta}
# Actualiza solamente los campos enviados.
@router.put(
    "/{id_receta}",
    response_model=RecetaRespuesta
)
def actualizar_receta(
    id_receta: int,
    datos: RecetaActualizar
):

    try:
        cambios = datos.model_dump(exclude_none=True)

        receta = dao.actualizar(
            id_receta,
            cambios
        )

        return receta

    except RecetaNoEncontradaError as ex:
        raise HTTPException(
            status_code=404,
            detail=str(ex)
        )


# DELETE /recetas/{id_receta}
# Elimina una receta si no está siendo utilizada por un postre.
@router.delete("/{id_receta}")
def eliminar_receta(id_receta: int):

    try:
        dao.eliminar(id_receta)

        return {
            "mensaje": f"Receta ID={id_receta} eliminada correctamente"
        }

    except RecetaNoEncontradaError as ex:
        raise HTTPException(
            status_code=404,
            detail=str(ex)
        )


# GET /recetas/{id_receta}/ingredientes
# Lista los ingredientes asociados a una receta.
@router.get("/{id_receta}/ingredientes")
def listar_ingredientes_receta(id_receta: int):

    receta = dao.buscar_por_id(id_receta)

    if not receta:
        raise HTTPException(
            status_code=404,
            detail=f"Receta ID={id_receta} no encontrada"
        )

    return dao.obtener_ingredientes(id_receta)


# POST /recetas/{id_receta}/ingredientes
# Agrega un ingrediente a una receta.
@router.post("/{id_receta}/ingredientes", status_code=201)
def agregar_ingrediente_receta(
    id_receta: int,
    datos: RecetaIngredienteCrear
):

    receta = dao.buscar_por_id(id_receta)

    if not receta:
        raise HTTPException(
            status_code=404,
            detail=f"Receta ID={id_receta} no encontrada"
        )

    dao.agregar_ingrediente(
        id_receta,
        datos.id_ingrediente,
        datos.cantidad
    )

    return {
        "mensaje": "Ingrediente agregado a la receta"
    }


# DELETE /recetas/{id_receta}/ingredientes/{id_ingrediente}
# Quita un ingrediente de una receta sin eliminar el ingrediente de la BD.
@router.delete(
    "/{id_receta}/ingredientes/{id_ingrediente}"
)
def quitar_ingrediente_receta(
    id_receta: int,
    id_ingrediente: int
):

    receta = dao.buscar_por_id(id_receta)

    if not receta:
        raise HTTPException(
            status_code=404,
            detail=f"Receta ID={id_receta} no encontrada"
        )

    dao.quitar_ingrediente(
        id_receta,
        id_ingrediente
    )

    return {
        "mensaje": "Ingrediente eliminado de la receta"
    }