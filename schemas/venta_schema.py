from pydantic import BaseModel, field_validator

from schemas.detalle_venta_schema import (
    DetalleVentaCrear,
    DetalleVentaRespuesta
)
# ----------------------------------------------------------------------
# SCHEMAS PYDANTIC - Venta
# Define y valida los datos que entran y salen de la API
# para el módulo de ventas.
# Las ventas se consideran registros históricos, por lo que
# no tienen schema de actualización ni de eliminación.
# ----------------------------------------------------------------------
# Lo que se envía al REGISTRAR una venta.
# React solamente envía los postres y sus cantidades.
# La fecha y el total son calculados automáticamente en el backend.
class VentaCrear(BaseModel):
    lineas: list[DetalleVentaCrear]

    @field_validator("lineas")
    @classmethod
    def validar_lineas(cls, valor):
        if len(valor) == 0:
            raise ValueError(
                "La venta debe contener al menos un postre"
            )
        return valor

# Lo que la API devuelve al consultar o registrar una venta.
class VentaRespuesta(BaseModel):
    id_venta: int
    fecha: str
    total: float
    detalle: list[DetalleVentaRespuesta]

# Respuesta utilizada para el módulo de reportes.
class VentaResumen(BaseModel):
    cantidad_ventas: int
    total_recaudado: float
    ventas: list