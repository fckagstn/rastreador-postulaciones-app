import { useState } from "react";
import { iniciarSesion } from "../servicios/api";
import { Link } from "react-router-dom";
import { useAuth } from "../contextos/AuthContexto";

function Login(){

    const [cargando, setCargando] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const [aviso, setAviso] = useState("")

    const [correo, setCorreo] = useState("")
    const [contrasena, setContrasena] = useState("")

    const { guardarToken } = useAuth()

    async function manejarLogin() {
        const listaAviso: string[] = []

        if (!correo) { listaAviso.push("Correo")}
        if (!contrasena) { listaAviso.push("Contraseña")}
        if (listaAviso.length > 0){
            setAviso("Llena los siguientes campos: " + listaAviso.join(', '))
            return
        }

        const datosLogin = {
            correo: correo,
            contrasena: contrasena
        }

        try {
            setCargando(true)
            const respuesta = await iniciarSesion(datosLogin)
            guardarToken(respuesta.access_token)
        }
        catch (error) {
            if (error instanceof Error){
                setError(error.message);
            } else {
                setError("Ocurrió un error inesperado")
            }
        }
        finally {
            setCargando(false)
        }
    }

    return (
        <div>
            <input 
                type="text"
                value={correo}
                onChange={evento => setCorreo(evento.target.value)}
                placeholder="usuario@example.com"/>

            <input 
                type="password"
                value={contrasena}
                onChange={evento => setContrasena(evento.target.value)}
                placeholder="Contraseña"/>

            {aviso && <p>{aviso}</p>}
            {cargando && <p>Espera un momento...</p>}
            {error && <p>Ocurrió un error: {error}</p>}

            <button onClick={manejarLogin}>Iniciar sesión</button>
            <Link to="/registro">¿No tienes cuenta? Regístrate</Link>
            
        </div>
    )

}

export default Login;