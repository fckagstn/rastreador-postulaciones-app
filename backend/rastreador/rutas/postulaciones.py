from fastapi import APIRouter, Depends
from rastreador.dependencias import obtener_sesion, obtener_usuario
from rastreador.esquemas import PostulacionEntrada, PostulacionSalida
from sqlalchemy import select
from rastreador.modelos_mapeados import Empresa, Postulacion, Portal, HistorialEstado

router = APIRouter(prefix="/postulaciones")

@router.post("", response_model=PostulacionSalida)
def registrar_postulacion(postulacion: PostulacionEntrada, session = Depends(obtener_sesion), usuario = Depends(obtener_usuario)):
    id_usuario = usuario.id

    # Buscar la empresa por nombre primero en la BD, con la empresa que dio el usuario
    empresa = postulacion.empresa.strip().lower()     # Normalizar a minusculas y eliminar residuos a los extremos del campo
    consulta_empresa = select(Empresa).where(Empresa.nombre_empresa == empresa)
    datos_empresa = session.scalars(consulta_empresa).first()

    # Si no hubo coincidencias, crear la empresa con la empresa que dio el usuario
    if datos_empresa is None:
        datos_empresa = Empresa(nombre_empresa = empresa)
        session.add(datos_empresa)
        session.commit()
        session.refresh(datos_empresa)

    # Buscar el portal por nombre primero en la BD, con el portal que dio el usuario, SI ES QUE LO DIO
    if postulacion.portal is not None:
        portal = postulacion.portal.strip().lower()
        consulta_portal = select(Portal).where(Portal.nombre_portal == portal)
        datos_portal = session.scalars(consulta_portal).first()

        # Si no hubo coincidencias, crear el portal con el portal que dio el usuario
        if datos_portal is None:
            datos_portal = Portal(nombre_portal = portal)
            session.add(datos_portal)
            session.commit()
            session.refresh(datos_portal)

    nueva_postulacion = Postulacion(
        puesto = postulacion.puesto,
        sueldo_centavos = postulacion.sueldo_centavos,
        empresa_id = datos_empresa.id,                     # Asignar el ID de la empresa extraida de la consulta o creada segun el caso
        estado_id = 1,                                     # Asignar el estado 'Postulado' por defecto en cada postulación, es el ID 1
        portal_id = datos_portal.id,
        usuario_id = id_usuario,
        mercado_id = postulacion.mercado_id,
        modalidad_id = postulacion.modalidad_id,
        fecha_postulacion = postulacion.fecha_postulacion
    )

    nuevo_historial = HistorialEstado(
        estado_id = nueva_postulacion.estado_id,
        postulacion_id = nueva_postulacion.id,
        fecha = nueva_postulacion.fecha_postulacion
    )

    try:
        session.add(nueva_postulacion)
        session.add(nuevo_historial)
        session.commit()
    except:
        raise

    return nueva_postulacion
    