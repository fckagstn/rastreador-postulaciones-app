from pydantic import BaseModel, Field, ConfigDict, EmailStr
from datetime import date, datetime

# =========USUARIOS ENTRADA Y SALIDA=============
class UsuarioEntrada(BaseModel):
    nombre: str
    apellidos: str
    correo: EmailStr
    contrasena: str = Field(max_length=72)

class UsuarioSalida(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str
    apellidos: str
    correo: EmailStr

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

class MercadoSalida(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str

class ModalidadSalida(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str

# =========POSTULACIONES ENTRADA ,SALIDA Y PARCHE==========
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

class PostulacionParche(BaseModel):
    puesto: str | None = Field(default=None, min_length=1)
    sueldo_centavos: int | None = None
    mercado_id: int | None = Field(default=None, ge=1)
    modalidad_id: int | None = Field(default=None, ge=1)
    fecha_postulacion: date | None = Field(default=None)

# =============ESTADO ENTRADA Y SALIDA===============
class EstadoEntrada(BaseModel):
    estado: str

class EstadoSalida(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre_estado: str

# ==========LOGIN ENTRADA==============
class LoginEntrada(BaseModel):
    correo: EmailStr
    contrasena: str

# =========HISTORIAL SALIDA=========
class HistorialSalida(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    estado: EstadoSalida
    fecha: datetime