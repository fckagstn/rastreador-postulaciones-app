import { useState } from "react"
import { iniciarSesion, registrarUsuario } from "../servicios/api"

interface Props{
    alIniciarSesion: (token: string) => void;
}

function Registro({ alIniciarSesion }: Props) {

    const [cargando, setCargando] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const [aviso, setAviso] = useState("")

    const [nombre, setNombre] = useState("")
    const [apellidos, setApellidos] = useState("")
    const [correo, setCorreo] = useState("")
    const [contrasena, setContrasena] = useState("")

    async function manejarRegistro() {
        const listaAviso: string[] = []

        if (!nombre) { listaAviso.push("Correo")}
        if (!apellidos) { listaAviso.push("Correo")}
        if (!correo) { listaAviso.push("Correo")}
        if (!contrasena) { listaAviso.push("Contraseña")}
        if (listaAviso.length > 0){
            setAviso("Llena los siguientes campos: " + listaAviso.join(', '))
            return
        }

        const datosRegistro = {
            nombre: nombre,
            apellidos: apellidos,
            correo: correo,
            contrasena: contrasena,
        }

        try {
            setCargando(true)
            const respuesta = await registrarUsuario(datosRegistro)

            const datosLogin = {
                correo: respuesta.correo,
                contrasena: contrasena,
            }

            const respuesta_login = await iniciarSesion(datosLogin)
            alIniciarSesion(respuesta_login.access_token)
        }
        catch (error) {
            if (error instanceof Error) {
                setError(error.message)
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
                value={nombre}
                onChange={evento => setNombre(evento.target.value)}
                placeholder="Tu nombre"/>

            <input 
                type="text"
                value={apellidos}
                onChange={evento => setApellidos(evento.target.value)}
                placeholder="Tus apellidos"/>

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

            <button onClick={manejarRegistro}>Registrarse</button>

            
        </div>
    )

}

export default Registro;