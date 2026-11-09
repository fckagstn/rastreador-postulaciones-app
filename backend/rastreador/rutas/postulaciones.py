from fastapi import APIRouter, Depends, HTTPException, Path
from rastreador.dependencias import obtener_sesion, obtener_usuario
from rastreador.esquemas import PostulacionEntrada, PostulacionSalida, PostulacionParche, EstadoEntrada, HistorialSalida, MercadoSalida, EstadoSalida
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from rastreador.modelos_mapeados import Empresa, Postulacion, Portal, HistorialEstado, Estado, Mercado
from datetime import datetime, timezone

router = APIRouter(prefix="/postulaciones")

@router.post("", response_model=PostulacionSalida, status_code=201)
def registrar_postulacion(postulacion: PostulacionEntrada, session = Depends(obtener_sesion), usuario = Depends(obtener_usuario)):
    id_usuario = usuario.id

    # Buscar la empresa por nombre primero en la BD, con la empresa que dio el usuario
    empresa = postulacion.empresa.strip().lower()     # Normalizar a minusculas y eliminar residuos a los extremos del campo
    consulta_empresa = select(Empresa).where(Empresa.nombre_empresa == empresa)
    la_empresa = session.scalars(consulta_empresa).first()

    # Si no hubo coincidencias, crear la empresa con la empresa que dio el usuario
    if la_empresa is None:
        la_empresa = Empresa(nombre_empresa = empresa)
        session.add(la_empresa)

    el_portal = None

    # Buscar el portal por nombre primero en la BD, con el portal que dio el usuario, SI ES QUE LO DIO
    if postulacion.portal is not None:
        portal = postulacion.portal.strip().lower()
        consulta_portal = select(Portal).where(Portal.nombre_portal == portal)
        el_portal = session.scalars(consulta_portal).first()

        # Si no hubo coincidencias, crear el portal con el portal que dio el usuario
        if el_portal is None:
            el_portal = Portal(nombre_portal = portal)
            session.add(el_portal)
            
    # Traer el estado 'postulado'
    consulta_estado = select(Estado).where(Estado.nombre_estado == "postulado")
    el_estado = session.scalars(consulta_estado).first()
    if el_estado is None:
        raise HTTPException(status_code=500, detail="No se ha creado el estado 'Postulado'")

    nueva_postulacion = Postulacion(
        puesto = postulacion.puesto,
        sueldo_centavos = postulacion.sueldo_centavos,
        empresa = la_empresa,               # Se pasan por medio de relationship sin usar su campo _id                  
        estado = el_estado,                 # Se pasan por medio de relationship sin usar su campo _id                            
        portal = el_portal,                 # Se pasan por medio de relationship sin usar su campo _id
        usuario_id = id_usuario,
        mercado_id = postulacion.mercado_id,
        modalidad_id = postulacion.modalidad_id,
        fecha_postulacion = postulacion.fecha_postulacion
    )

    nuevo_historial = HistorialEstado(
        estado = el_estado,                  # Se pasan por medio de relationship sin usar su campo _id
        postulacion = nueva_postulacion,        # Se pasan por medio de relationship sin usar su campo _id
        fecha = datetime.now(timezone.utc)
    )

    # Agregar todo y commitear la BD
    session.add(nueva_postulacion)
    session.add(nuevo_historial)
    session.commit()
    
    return nueva_postulacion

@router.get("", response_model=list[PostulacionSalida])
def listar_postulaciones(usuario = Depends(obtener_usuario), session = Depends(obtener_sesion)):
    id_usuario = usuario.id

    # Traer las postulaciones usando el id extraido del token 
    consulta_postulaciones = (
        select(Postulacion)
        .where(Postulacion.usuario_id == id_usuario).
        options(
            joinedload(Postulacion.empresa),
            joinedload(Postulacion.estado),
            joinedload(Postulacion.portal),
            joinedload(Postulacion.mercado),
            joinedload(Postulacion.modalidad)
        )
    )

    datos_postulaciones = session.scalars(consulta_postulaciones).all()

    return datos_postulaciones

@router.get("/{id}", response_model=PostulacionSalida)
def traer_postulacion(id: int = Path(ge=1), usuario = Depends(obtener_usuario), session = Depends(obtener_sesion)):
    id_usuario = usuario.id
    consulta_postulacion = select(Postulacion).where(Postulacion.id == id, Postulacion.usuario_id == id_usuario)
    la_postulacion = session.scalars(consulta_postulacion).first()

    if la_postulacion is None:
            raise HTTPException(status_code=404, detail="No existe la postulación que buscas")

    return la_postulacion

@router.patch("/{id}", response_model=PostulacionSalida)
def actualizar_parcial_postulacion(
    postulacion: PostulacionParche, 
    id: int = Path(ge=1), 
    usuario = Depends(obtener_usuario), 
    session = Depends(obtener_sesion)
):
    id_usuario = usuario.id

    # Buscar la postulacion para evaluar si su condicion es None o se procede a actualizar
    consulta_postulacion = select(Postulacion).where(Postulacion.id == id, Postulacion.usuario_id == id_usuario)
    la_postulacion = session.scalars(consulta_postulacion).first()
    if la_postulacion is None:
        raise HTTPException(status_code=404, detail="No existe la postulación que buscas")

    datos = postulacion.model_dump(exclude_unset=True)
    if not datos:
        raise HTTPException(status_code=422, detail="Los datos proporcionados no son válidos")

    for clave, valor in datos.items():
        setattr(la_postulacion, clave, valor)

    session.commit()
    return la_postulacion

@router.patch("/{id}/estado", response_model=PostulacionSalida)
def actualizar_estado_postulacion(
    estado: EstadoEntrada, 
    id: int = Path(ge=1), 
    usuario = Depends(obtener_usuario), 
    session = Depends(obtener_sesion)
):
    id_usuario = usuario.id

    consulta_postulacion = select(Postulacion).where(Postulacion.id == id, Postulacion.usuario_id == id_usuario)
    la_postulacion = session.scalars(consulta_postulacion).first()
    if la_postulacion is None:
        raise HTTPException(status_code=404, detail="No existe la postulacion que buscas")

    nombre = estado.estado.strip().lower()
    consulta_estado = select(Estado).where(Estado.nombre_estado == nombre)
    el_estado = session.scalars(consulta_estado).first()
    if el_estado is None:
        raise HTTPException(status_code=422, detail="Los datos proporcionados no son válidos para procesar la solicitud")

    la_postulacion.estado = el_estado

    nuevo_historial = HistorialEstado(
        estado = el_estado,
        postulacion = la_postulacion,
        fecha = datetime.now(timezone.utc)
    )

    session.add(nuevo_historial)
    session.commit()
    return la_postulacion

@router.delete("/{id}", status_code=204)
def borrar_postulacion(id: int = Path(ge=1), usuario = Depends(obtener_usuario), session = Depends(obtener_sesion)):
    id_usuario = usuario.id
    consulta_postulacion = select(Postulacion).where(Postulacion.id == id, Postulacion.usuario_id == id_usuario)
    la_postulacion = session.scalars(consulta_postulacion).first()
    if la_postulacion is None:
        raise HTTPException(status_code=404, detail="No existe la postulacion que deseas eliminar")

    session.delete(la_postulacion)
    session.commit()

@router.get("/{id}/historial", response_model=list[HistorialSalida])
def traer_historial(id: int = Path(ge=1), usuario = Depends(obtener_usuario), session = Depends(obtener_sesion)):
    id_usuario = usuario.id

    consulta_postulacion = select(Postulacion).where(Postulacion.id == id, Postulacion.usuario_id == id_usuario)
    la_postulacion = session.scalars(consulta_postulacion).first()
    if la_postulacion is None:
        raise HTTPException(status_code=404, detail="No existe la postulacion que buscas")
    
    consulta_historial = select(HistorialEstado).where(HistorialEstado.postulacion_id == id).order_by(HistorialEstado.fecha)
    el_historial = session.scalars(consulta_historial).all()
    return el_historial

@router.get("/mercados", response_model=list[MercadoSalida])
def traer_mercados(session = Depends(obtener_sesion)):
    consulta_mercados = select(Mercado)
    los_mercados = session.scalars(consulta_mercados).all()
    return los_mercados

@router.get("/estados", response_model=list[EstadoSalida])
def traer_estados(session = Depends(obtener_sesion)):
    consulta_estados = select(Estado)
    los_estados = session.scalars(consulta_estados).all()
    return los_estados