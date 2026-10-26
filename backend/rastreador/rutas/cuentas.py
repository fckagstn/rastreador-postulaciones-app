from fastapi import APIRouter, Depends, HTTPException  
from rastreador.esquemas import UsuarioEntrada, UsuarioSalida
from rastreador.dependencias import obtener_sesion
from rastreador.seguridad import hashear_contrasena
from rastreador.modelos_mapeados import Usuario
from sqlalchemy.exc import IntegrityError

router = APIRouter()

@router.post("/usuarios", status_code=201, response_model=UsuarioSalida)        
def crear_nuevo_usuario(usuario: UsuarioEntrada, session = Depends(obtener_sesion)):
    # Extraer la contraseña, guardar en una variable y hashearla llamando la función desde 'rastreador.seguridad'
    contrasena = usuario.contrasena
    hashed_contrasena = hashear_contrasena(contrasena)

    # Registrar ese nuevo usuario e intentar registrarlo en la BD
    nuevo_usuario = Usuario(
        nombre = usuario.nombre,
        apellidos = usuario.apellidos,
        correo = usuario.correo,
        contrasena_hashed = hashed_contrasena
    )

    try:
        session.add(nuevo_usuario)
        session.commit()

    # Camino por si es un error de duplicado (UNIQUE)
    except IntegrityError as e:
        session.rollback()
        if isinstance(e.orig, IntegrityError):
            raise HTTPException(
                status_code=409,
                detail="El correo no se encuentra disponible, prueba con otro"
            )

        raise

    return nuevo_usuario