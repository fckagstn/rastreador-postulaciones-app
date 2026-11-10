from fastapi import APIRouter, Depends
from rastreador.esquemas import MercadoSalida, EstadoSalida, ModalidadSalida
from rastreador.modelos_mapeados import Mercado, Estado, Modalidad
from rastreador.dependencias import obtener_sesion
from sqlalchemy import select

router = APIRouter()

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

@router.get("/modalidades", response_model=list[ModalidadSalida])
def traer_modalidades(session = Depends(obtener_sesion)):
    consulta_modalidades = select(Modalidad)
    las_modalidades = session.scalars(consulta_modalidades).all()
    return las_modalidades
