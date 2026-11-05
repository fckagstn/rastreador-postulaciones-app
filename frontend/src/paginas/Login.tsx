import { useState } from "react";
import { iniciarSesion } from "../servicios/api";

interface Props{
    alIniciarSesion: (token: string) => void;
}

function Login({ alIniciarSesion }: Props){

    const [cargando, setCargando] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const [aviso, setAviso] = useState("")

    const [correo, setCorreo] = useState("")
    const [contrasena, setContrasena] = useState("")

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

            <button onClick={() => {
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

                async function login() {
                    try {
                        setCargando(true)
                        const respuesta = await iniciarSesion(datosLogin)
                        alIniciarSesion(respuesta.access_token)
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
                login()
            }}>Iniciar sesión</button>
        </div>
    )

}

export default Login;