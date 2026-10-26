from pydantic import BaseModel, Field, ConfigDict
from datetime import date

# =========USUARIOS ENTRADA Y SALIDA=============
class UsuarioEntrada(BaseModel):
    nombre: str
    apellidos: str
    correo: str
    contrasena: str = Field(max_length=72)

class UsuarioSalida(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str
    apellidos: str
    correo: str

# =========PORTALES ENTRADA Y SALIDA============
class PortalEntrada(BaseModel):
    nombre_portal: str

class PortalSalida(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre_portal: str

# ==========CATALOGOS SALIDAS===============
class EmpresaSalida(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre_empresa: str

class EstadoSalida(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre_estado: str

class MercadoSalida(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str

class ModalidadSalida(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str

# =========POSTULACIONES ENTRADA Y SALIDA==========
class PostulacionEntrada(BaseModel):
    puesto: str
    sueldo_centavos: int | None = Field(ge=1, default=None)
    empresa: str
    portal: str | None = Field(default=None)
    mercado_id: int | None = Field(default=None)
    modalidad_id: int | None = Field(default=None)
    fecha_postulacion: date

class PostulacionSalida(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    puesto: str
    sueldo_centavos: int | None
    empresa: EmpresaSalida
    estado: EstadoSalida
    portal: PortalSalida | None
    mercado: MercadoSalida | None
    modalidad: ModalidadSalida | None
    fecha_postulacion : date

# ==========LOGIN ENTRADA==============
class LoginEntrada(BaseModel):
    correo: str
    contrasena: str
    