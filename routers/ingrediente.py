from fastapi import APIRouter, HTTPException

from dao.ingrediente_dao import (
    IngredienteDAO,
    IngredienteNoEncontradoError,
)
from modelos.ingrediente import Ingrediente
from schemas.ingrediente_schema import (
    IngredienteCrear,
    IngredienteActualizar,
    IngredienteRespuesta,
)
# ----------------------------------------------------------------------
# ROUTER - Ingredientes
# Define los endpoints HTTP para gestionar ingredientes.
# ----------------------------------------------------------------------
router = APIRouter(
    prefix="/ingredientes",
    tags=["Ingredientes"]
)
dao = IngredienteDAO()
# GET /ingredientes/
# Lista todos los ingredientes registrados.
@router.get("/", response_model=list[IngredienteRespuesta])
def listar_ingredientes():
    return dao.obtener_todos()

# GET /ingredientes/{id_ingrediente}
# Busca un ingrediente específico por su ID.
@router.get("/{id_ingrediente}", response_model=IngredienteRespuesta)
def obtener_ingrediente(id_ingrediente: int):
    ingrediente = dao.buscar_por_id(id_ingrediente)

    if not ingrediente:
        raise HTTPException(
            status_code=404,
            detail=f"Ingrediente ID={id_ingrediente} no encontrado"
        )

    return ingrediente

# POST /ingredientes/
# Registra un nuevo ingrediente.
@router.post(
    "/",
    response_model=IngredienteRespuesta,
    status_code=201
)
def crear_ingrediente(datos: IngredienteCrear):
    ingrediente = Ingrediente(
        datos.nombre,
        datos.unidad_medida,
        datos.stock_actual,
        datos.stock_minimo,
        datos.costo
    )

    nuevo = dao.insertar(ingrediente)

    return nuevo.to_dict()

# PUT /ingredientes/{id_ingrediente}
# Actualiza solamente los campos enviados.
@router.put(
    "/{id_ingrediente}",
    response_model=IngredienteRespuesta
)
def actualizar_ingrediente(
    id_ingrediente: int,
    datos: IngredienteActualizar
):
    try:
        cambios = datos.model_dump(exclude_none=True)

        ingrediente = dao.actualizar(
            id_ingrediente,
            cambios
        )

        return ingrediente

    except IngredienteNoEncontradoError as ex:
        raise HTTPException(
            status_code=404,
            detail=str(ex)
        )
# DELETE /ingredientes/{id_ingrediente}
# Elimina un ingrediente si no está siendo utilizado por una receta.
@router.delete("/{id_ingrediente}")
def eliminar_ingrediente(id_ingrediente: int):
    try:
        dao.eliminar(id_ingrediente)

        return {
            "mensaje": f"Ingrediente ID={id_ingrediente} eliminado"
        }

    except IngredienteNoEncontradoError as ex:
        raise HTTPException(
            status_code=404,
            detail=str(ex)
        )