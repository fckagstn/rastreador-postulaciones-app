import { useState, useEffect } from "react";
import type { PostulacionSalida } from "../tipos/api";
import { listarPostulaciones } from "../servicios/api";
import TarjetaPostulacion from "../componentes/TarjetaPostulacion";

interface Props{
    token: string;
    removerToken: () => void;
    contador: number;
}

function ListarPostulaciones({ token, removerToken, contador }: Props){

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
    }, [token, contador])

    return (
        <div>
            {cargando && <p>Cargando postulaciones...</p>}
            {error && <p>Ocurrió un error: { error }</p>}
            {postulaciones.length > 0 ? postulaciones.map(postulacion => <TarjetaPostulacion key={postulacion.id} postulacion={postulacion}/>) : <p>No tienes postulaciones registradas</p>}
            <button onClick={removerToken}>Cerrar sesión</button>
        </div>
    )
}

export default ListarPostulaciones;