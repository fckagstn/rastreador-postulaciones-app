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

# ==========CATALOGOS SALIDAS===============
class EmpresaSalida(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre_empresa: str

class EstadoSalida(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre_estado: str

class PortalSalida(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre_portal: str

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
    precio_centavos: int | None = Field(ge=1)
    empresa = int | str
    estado_id = int
    portal_id = int | None
    usuario_id = int
    mercado_id = int | None
    modalidad_id = int | None
    fecha_postulacion = date

class PostulacionSalida(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    puesto: str
    precio_centavos: int | None
    empresa: EmpresaSalida
    estado: EstadoSalida
    portal: PortalSalida | None
    usuario: UsuarioSalida
    mercado: MercadoSalida | None
    modalidad: ModalidadSalida | None
    fecha_postulacion : date

