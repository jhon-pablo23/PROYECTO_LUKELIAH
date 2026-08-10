from pydantic import BaseModel, field_validator
from typing import Optional


# ----------------------------------------------------------------------
# SCHEMAS PYDANTIC - Postre
#
# Define y valida los datos que entran y salen de la API
# para el módulo de postres.
# ----------------------------------------------------------------------


# Lo que se envía al CREAR un postre
class PostreCrear(BaseModel):
    id_receta: int
    nombre: str
    precio: float
    imagen: Optional[str] = None

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, valor):
        if not valor.strip():
            raise ValueError("El nombre no puede estar vacío")
        return valor

    @field_validator("precio")
    @classmethod
    def validar_precio(cls, valor):
        if valor < 0:
            raise ValueError("El precio no puede ser negativo")
        return valor


# Lo que se envía al ACTUALIZAR un postre
class PostreActualizar(BaseModel):
    id_receta: Optional[int] = None
    nombre: Optional[str] = None
    precio: Optional[float] = None
    imagen: Optional[str] = None

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, valor):
        if valor is not None and not valor.strip():
            raise ValueError("El nombre no puede estar vacío")
        return valor

    @field_validator("precio")
    @classmethod
    def validar_precio(cls, valor):
        if valor is not None and valor < 0:
            raise ValueError("El precio no puede ser negativo")
        return valor


# Lo que la API devuelve como respuesta
class PostreRespuesta(BaseModel):
    id_postre: int
    id_receta: int
    nombre: str
    precio: float
    imagen: Optional[str] = None