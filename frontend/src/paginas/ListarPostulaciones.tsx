import { useState, useEffect } from "react";
import type { PostulacionSalida } from "../tipos/api";
import { listarPostulaciones } from "../servicios/api";

interface Props{
    token: string;
}

function ListarPostulaciones({ token }: Props){

    const [postulaciones, setPostulaciones] = useState<PostulacionSalida[]>([])
    const [error, setError] = useState<string | null>(null)
    const [cargando, setCargando] = useState(false)
    
    useEffect(() => {
        async function manejarPostulaciones() {
            try{
                setCargando(true)
                const respuesta = await listarPostulaciones(token)
                setPostulaciones(respuesta)
            }
            catch (error){
                if (error instanceof Error) {
                    setError(error.message)
                } else {
                    setError("Ocurrió un error inesperado")
                }
            }
            finally {
                setCargando(false)
            }
        } manejarPostulaciones()
    }, [token])

    return (
        <div>
            {cargando && <p>Cargando postulaciones...</p>}
            {error && <p>Ocurrió un error: { error }</p>}
            {postulaciones && postulaciones.map(dato => <h3 key={dato.id}>{dato.puesto}</h3>)}
        </div>
    )
}

export default ListarPostulaciones;