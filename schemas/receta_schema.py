from pydantic import BaseModel, field_validator
from typing import Optional


# ----------------------------------------------------------------------
# SCHEMAS PYDANTIC - Receta
#
# Define y valida los datos que entran y salen de la API
# para el módulo de recetas.
# ----------------------------------------------------------------------


# Lo que se envía al CREAR una receta
class RecetaCrear(BaseModel):
    nombre: str
    porciones: int
    procedimiento: str

    # Una receta debe producir al menos una porción.
    @field_validator("porciones")
    @classmethod
    def validar_porciones(cls, valor):
        if valor <= 0:
            raise ValueError("Las porciones deben ser mayores a 0")
        return valor


# Lo que se envía al ACTUALIZAR una receta
class RecetaActualizar(BaseModel):
    # Los campos son opcionales para permitir modificar
    # solamente los datos necesarios.
    nombre: Optional[str] = None
    porciones: Optional[int] = None
    procedimiento: Optional[str] = None

    @field_validator("porciones")
    @classmethod
    def validar_porciones(cls, valor):
        if valor is not None and valor <= 0:
            raise ValueError("Las porciones deben ser mayores a 0")
        return valor


# Lo que la API devuelve como respuesta
class RecetaRespuesta(BaseModel):
    id_receta: int
    nombre: str
    porciones: int
    procedimiento: str