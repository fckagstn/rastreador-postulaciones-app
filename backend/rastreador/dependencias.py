from fastapi import HTTPException, Depends, Header
import jwt
from sqlalchemy.orm import Session
from rastreador.modelos_mapeados import engine, Usuario
from rastreador.seguridad import leer_token

# Función para obtener una conexión con la BD que sera usada por toda la app 
def obtener_sesion():
    with Session(engine) as session:
        yield session

def obtener_usuario(authorization: str | None = Header(None), session = Depends(obtener_sesion)):   # Parámetro 'authorization' para poder leer las credenciales de autorización establecido 'None' por defecto

    # Cortar el programa si no se mando la cabecera 'authorization'
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="No se mando la cabecera autorización",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token_partes = authorization.split(" ")       # Si se mando la cabecera, separar el formato para obtener '['Bearer', 'mi_token_secreto_123']'

    # Si el tamaño de la lista 'token_partes' es diferente de 2 o si el primer elemento de la lista es diferente de 'bearer', cortar el programa
    if len(token_partes) != 2 or token_partes[0] != "bearer":   
        raise HTTPException(
            status_code=401,
            detail="Formato de token invalido. Usa 'Bearer <token>'",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = token_partes[1]             # Del formato '['Bearer', 'mi_token_secreto_123']', extraer el token

    try:
        # Extraer el sub y asignarlo a la variable 'id_usuario' usando la función 'leer_token' 
        id_usuario = leer_token(token)

    # Camino por si el token esta expirado
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="El token ha expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Camino por si se intento modificar el token cambiando el formato
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401, 
            detail="El token proporcionado es invalido o esta corrupto", 
            headers={"WWW-Authenticate": "Bearer"}
        )

    usuario = session.get(Usuario, id_usuario)          # Buscar la información del usuario por medio del id que se obtuvo

    # Si no existe el usuario, cortar el programa
    if usuario is None:
        raise HTTPException(
            status_code=401,
            detail="No fue posible encontrar al usuario",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return usuario
