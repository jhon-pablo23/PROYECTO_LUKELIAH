from pydantic import BaseModel, field_validator
from typing import Optional


# ----------------------------------------------------------------------
# SCHEMAS PYDANTIC - RecetaIngrediente
#
# Define y valida los datos de la relación entre
# una receta y sus ingredientes.
# ----------------------------------------------------------------------


# Lo que se envía al AGREGAR un ingrediente a una receta
class RecetaIngredienteCrear(BaseModel):
    id_receta: int
    id_ingrediente: int
    cantidad: float

    @field_validator("id_receta", "id_ingrediente")
    @classmethod
    def validar_ids(cls, valor):
        if valor <= 0:
            raise ValueError("El ID debe ser mayor a 0")
        return valor

    @field_validator("cantidad")
    @classmethod
    def validar_cantidad(cls, valor):
        if valor <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        return valor


# Lo que se envía al ACTUALIZAR la cantidad
class RecetaIngredienteActualizar(BaseModel):
    cantidad: Optional[float] = None

    @field_validator("cantidad")
    @classmethod
    def validar_cantidad(cls, valor):
        if valor is not None and valor <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        return valor


# Lo que la API devuelve como respuesta
class RecetaIngredienteRespuesta(BaseModel):
    id_receta: int
    id_ingrediente: int
    cantidad: float