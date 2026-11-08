from fastapi import HTTPException, Depends, Header
import jwt
from sqlalchemy.orm import Session
from rastreador.modelos_mapeados import engine, Usuario
from rastreador.seguridad import leer_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

# Función para obtener una conexión con la BD que sera usada por toda la app 
def obtener_sesion():
    with Session(engine) as session:
        yield session

def obtener_usuario(credenciales: HTTPAuthorizationCredentials = Depends(security), session = Depends(obtener_sesion)):   

    token = credenciales.credentials

    try:
        # Extraer el sub y asignarlo a la variable 'id_usuario' usando la función 'leer_token' 
        id_usuario = leer_token(token)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="El token ha expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401, 
            detail="El token proporcionado es inválido o está corrupto", 
            headers={"WWW-Authenticate": "Bearer"}
        )

    usuario = session.get(Usuario, id_usuario)

    if usuario is None:
        raise HTTPException(
            status_code=401,
            detail="No fue posible encontrar al usuario",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return usuario
