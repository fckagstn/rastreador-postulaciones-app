import type { UsuarioEntrada, UsuarioSalida } from "../tipos/api";

const apiUrl = import.meta.env.VITE_API_URL

export async function registrarUsuario(usuario: UsuarioEntrada): Promise<UsuarioSalida> {
    const respuesta = await fetch(`${apiUrl}/usuarios`, {
        method: "POST",
        headers: {
            "Content-type": "application/json",
        },
        body: JSON.stringify(usuario),
    });

    if (!respuesta.ok){
        const cuerpo = await respuesta.json();
        throw new Error(cuerpo.detail);
    }
    return respuesta.json()
}

