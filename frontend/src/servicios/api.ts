import type { UsuarioEntrada, UsuarioSalida, LoginEntrada, PostulacionSalida, TokenSalida } from "../tipos/api";

const apiUrl = import.meta.env.VITE_API_URL

function cabecera(token: string){
    const cabecera = { "Authorization": "Bearer " + token }
    return cabecera
}

async function verificarRespuesta(respuesta: Response){
    if (!respuesta.ok){
        const cuerpo = await respuesta.json()
        throw new Error(cuerpo.detail)
    }
}

export async function registrarUsuario(usuario: UsuarioEntrada): Promise<UsuarioSalida> {
    const respuesta = await fetch(`${apiUrl}/usuarios`, {
        method: "POST",
        headers: {
            "Content-type": "application/json",
        },
        body: JSON.stringify(usuario),
    });

    await verificarRespuesta(respuesta)
    return respuesta.json()
}

export async function iniciarSesion(datos: LoginEntrada): Promise<TokenSalida> {
    const respuesta = await fetch(`${apiUrl}/login`, {
        method: "POST",
        headers: {
            "Content-type": "application/json",
        },
        body: JSON.stringify(datos),
    });

    await verificarRespuesta(respuesta)
    return respuesta.json()
}

export async function obtenerPerfil(token: string): Promise<UsuarioSalida> {
    const respuesta = await fetch(`${apiUrl}/perfil`, {
        method: "GET",
        headers: cabecera(token),
    });
    await verificarRespuesta(respuesta)
    return respuesta.json()
}

export async function listarPostulaciones(token: string): Promise<PostulacionSalida[]> {
    const respuesta = await fetch(`${apiUrl}/postulaciones`, {
        method: "GET",
        headers: cabecera(token),
    });
    await verificarRespuesta(respuesta)
    return respuesta.json()
}
