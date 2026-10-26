from fastapi import APIRouter, Depends, HTTPException  
from rastreador.esquemas import UsuarioEntrada, UsuarioSalida, LoginEntrada
from rastreador.dependencias import obtener_sesion, obtener_usuario
from rastreador.seguridad import hashear_contrasena, hash_senuelo, verificar_contrasena, crear_token
from rastreador.modelos_mapeados import Usuario
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

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

@router.post("/login")
def loguearse(datos: LoginEntrada, session = Depends(obtener_sesion)):
    # Traer los datos del usuario donde el correo sea igual en la BD
    consulta = select(Usuario).where(Usuario.correo == datos.correo)
    datos_usuario = session.scalars(consulta).first()

    # Si no se encontro el usuario, usar el 'hash_senuelo' por el canal de tiempo para simular el tiempo de respuesta y cortar el programa
    if datos_usuario is None:
        verificar_contrasena(datos.contrasena, hash_senuelo)
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Guardar el valor True o False a la validación de contraseñas y usarlo para decidir que hacer
    validacion = verificar_contrasena(datos.contrasena, datos_usuario.contrasena_hashed)

    if validacion:
        token = crear_token(datos_usuario.id)
        datos_login = {
            "access_token": token,
            "token_type": "Bearer"
        }
        return datos_login

    else:
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"}
        )

@router.get("/perfil", response_model=UsuarioSalida)
def leer_perfil(usuario = Depends(obtener_usuario)):
    return usuario