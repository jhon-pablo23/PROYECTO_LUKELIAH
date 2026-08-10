import re
from pydantic import BaseModel, field_validator
from typing import Optional

# ----------------------------------------------------------------------
# SCHEMAS PYDANTIC - Usuario
#
# Los schemas definen la estructura de los datos que entran y salen
# de la API. Pydantic valida automáticamente los datos recibidos.
# ----------------------------------------------------------------------

# Lo que se envía al CREAR un usuario
class UsuarioCrear(BaseModel):
    nombre: str
    correo: str
    contrasena: str

    # Valida que el correo tenga un formato correcto.
    @field_validator("correo")
    @classmethod
    def validar_correo(cls, valor):
        if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", valor):
            raise ValueError(
                "El correo no tiene un formato válido "
                "(ej: nombre@dominio.com)"
            )
        return valor


# Lo que se envía al ACTUALIZAR un usuario
class UsuarioActualizar(BaseModel):
    # Los campos son opcionales para permitir modificar
    # solamente los datos necesarios.
    nombre: Optional[str] = None
    correo: Optional[str] = None
    contrasena: Optional[str] = None


# Lo que la API devuelve como respuesta
class UsuarioRespuesta(BaseModel):
    # La contraseña no se devuelve por seguridad.
    id_usuario: int
    nombre: str
    correo: str


# Datos necesarios para iniciar sesión
class UsuarioLogin(BaseModel):
    correo: str
    contrasena: str