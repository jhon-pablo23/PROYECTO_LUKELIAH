from pydantic import BaseModel, field_validator
# ----------------------------------------------------------------------
# SCHEMAS PYDANTIC - DetalleVenta
# Define y valida los datos correspondientes a los postres
# incluidos dentro de una venta.
# ----------------------------------------------------------------------

# Datos de cada postre que React envía al registrar una venta.
class DetalleVentaCrear(BaseModel):
    id_postre: int
    cantidad: int

    @field_validator("cantidad")
    @classmethod
    def validar_cantidad(cls, valor):
        if valor <= 0:
            raise ValueError(
                "La cantidad debe ser mayor a 0"
            )
        return valor

# Datos que la API devuelve de cada detalle.
class DetalleVentaRespuesta(BaseModel):
    id_detalle: int
    id_postre: int
    nombre: str
    cantidad: int
    precio: float
    subtotal: float