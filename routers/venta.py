from datetime import date

from fastapi import APIRouter, HTTPException

from dao.venta_dao import VentaDAO
from schemas.venta_schema import (
    VentaCrear,
    VentaRespuesta,
    VentaResumen
)

# ----------------------------------------------------------------------
# ROUTER - Venta
# Define los endpoints HTTP para registrar y consultar ventas.
#
# Las ventas se consideran registros históricos:
# se pueden registrar y consultar, pero no editar ni eliminar.
# ----------------------------------------------------------------------

router = APIRouter(
    prefix="/ventas",
    tags=["Ventas"]
)

dao = VentaDAO()

# ----------------------------------------------------------------------
# GET /ventas/
# Lista todas las ventas registradas.
# Cada venta incluye también sus detalles.
# ----------------------------------------------------------------------

@router.get(
    "/",
    response_model=list[VentaRespuesta]
)
def listar_ventas():
    return dao.obtener_todos()

# ----------------------------------------------------------------------
# GET /ventas/resumen
# Obtiene un resumen de ventas dentro de un rango de fechas.
# Esta ruta debe estar ANTES de /{id_venta} para que FastAPI
# no intente interpretar la palabra "resumen" como un ID.
# ----------------------------------------------------------------------

@router.get(
    "/resumen",
    response_model=VentaResumen
)
def obtener_resumen(
    fecha_inicio: date,
    fecha_fin: date
):
    return dao.obtener_resumen(
        fecha_inicio,
        fecha_fin
    )
# ----------------------------------------------------------------------
# GET /ventas/{id_venta}

# Busca una venta específica por su ID.
# También devuelve los detalles asociados a la venta.
# ----------------------------------------------------------------------

@router.get(
    "/{id_venta}",
    response_model=VentaRespuesta
)
def obtener_venta(id_venta: int):

    venta = dao.buscar_por_id(id_venta)

    if not venta:
        raise HTTPException(
            status_code=404,
            detail=f"Venta ID={id_venta} no encontrada"
        )

    return venta

# ----------------------------------------------------------------------
# POST /ventas/
# Registra una venta nueva.

# Reat envía únicamente:
# - id_postre
# - cantidad
#
# El DAO se encarga de:
# - consultar el precio real del postre
# - calcular el total
# - generar la fecha
# - registrar la venta
# - registrar sus detalles
# ----------------------------------------------------------------------
@router.post(
    "/",
    response_model=VentaRespuesta,
    status_code=201
)
def registrar_venta(datos: VentaCrear):
    # Convierte los objetos Pydantic a diccionarios porque
    # VentaDAO.registrar() recibe una lista de diccionarios.
    lineas = [
        linea.model_dump()
        for linea in datos.lineas
    ]
    try:
        return dao.registrar(lineas)

    except ValueError as ex:
        raise HTTPException(
            status_code=404,
            detail=str(ex)
        )