from pydantic import BaseModel, field_validator

from schemas.detalle_venta_schema import (
    DetalleVentaCrear,
    DetalleVentaRespuesta
)


# ----------------------------------------------------------------------
# SCHEMAS PYDANTIC - Venta
#
# Una venta recibe una lista de postres con sus cantidades.
# La fecha y el total son calculados automáticamente por el backend.
#
# Las ventas se conservan como historial, por lo que no tienen
# schema de actualización ni de eliminación.
# ----------------------------------------------------------------------


# Lo que se envía al REGISTRAR una venta
class VentaCrear(BaseModel):
    lineas: list[DetalleVentaCrear]

    @field_validator("lineas")
    @classmethod
    def validar_lineas(cls, valor):
        if len(valor) == 0:
            raise ValueError("La venta debe contener al menos un postre")
        return valor


# Lo que la API devuelve
class VentaRespuesta(BaseModel):
    id_venta: int
    fecha: str
    total: float
    detalle: list[DetalleVentaRespuesta]