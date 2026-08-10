from pydantic import BaseModel, field_validator
from typing import Optional


# ----------------------------------------------------------------------
# SCHEMAS PYDANTIC - Ingrediente
#
# Define y valida los datos que entran y salen de la API
# para el módulo de ingredientes.
# ----------------------------------------------------------------------


class IngredienteCrear(BaseModel):
    nombre: str
    unidad_medida: str
    stock_actual: float
    stock_minimo: float
    costo: float

    @field_validator("unidad_medida")
    @classmethod
    def validar_unidad_medida(cls, valor):
        unidades_validas = ["kg", "g", "ml", "L", "unidad"]

        if valor not in unidades_validas:
            raise ValueError(
                "La unidad de medida debe ser: kg, g, ml, L o unidad"
            )

        return valor

    @field_validator("stock_actual", "stock_minimo", "costo")
    @classmethod
    def validar_no_negativo(cls, valor):
        if valor < 0:
            raise ValueError("El valor no puede ser negativo")

        return valor


class IngredienteActualizar(BaseModel):
    nombre: Optional[str] = None
    unidad_medida: Optional[str] = None
    stock_actual: Optional[float] = None
    stock_minimo: Optional[float] = None
    costo: Optional[float] = None

    @field_validator("unidad_medida")
    @classmethod
    def validar_unidad_medida(cls, valor):
        if valor is None:
            return valor

        unidades_validas = ["kg", "g", "ml", "L", "unidad"]

        if valor not in unidades_validas:
            raise ValueError(
                "La unidad de medida debe ser: kg, g, ml, L o unidad"
            )

        return valor

    @field_validator("stock_actual", "stock_minimo", "costo")
    @classmethod
    def validar_no_negativo(cls, valor):
        if valor is not None and valor < 0:
            raise ValueError("El valor no puede ser negativo")

        return valor


class IngredienteRespuesta(BaseModel):
    id_ingrediente: int
    nombre: str
    unidad_medida: str
    stock_actual: float
    stock_minimo: float
    costo: float