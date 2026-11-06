import type { PostulacionSalida } from "../tipos/api";

interface Props {
    postulacion: PostulacionSalida;
}

function TarjetaPostulacion({ postulacion }: Props){

    return (
        <div key={postulacion.id}>
            <h3>{postulacion.puesto}</h3>
            {postulacion.sueldo_centavos ? <p>{postulacion.sueldo_centavos / 100.0}</p>: <p>No hay sueldo registrado para esta postulación</p>}
            <p>Empresa: {postulacion.empresa.nombre_empresa}</p>
            <p>Estado de la postulación: {postulacion.estado.nombre_estado}</p>
            {postulacion.portal ? <p>Portal: {postulacion.portal.nombre_portal}</p> : <p>No se registro el portal para esta postulación</p>}
            {postulacion.mercado ? <p>Tipo de mercado: {postulacion.mercado.nombre}</p> : <p>No se registro el tipo de mercado para esta postulación</p>}
            {postulacion.modalidad ? <p>Tipo de modalidad: {postulacion.modalidad.nombre}</p> : <p>No se registro el tipo de modalidad para esta postulación</p>}
        </div>
    )
}

export default TarjetaPostulacion;