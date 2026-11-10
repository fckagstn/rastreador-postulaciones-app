
import { useState, useEffect } from "react"
import { crearPostulacion, listarMercados, listarModalidades } from "../servicios/api"
import { type MercadoSalida, type ModalidadSalida } from "../tipos/api"

interface Props {
    token: string;
    subirContador: () => void;
}

function NuevaPostulacion({ token, subirContador }: Props){

    // AVISOS
    const [cargando, setCargando] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const [aviso, setAviso] = useState("")
    const [exito, setExito] = useState("")

    // CATALOGOS
    const [mercados, setMercados] = useState<MercadoSalida[]>([])
    const [modalidades, setModalidades] = useState<ModalidadSalida[]>([])

    // DATOS DEL FORMULARIO
    const [puesto, setPuesto] = useState("")
    const [sueldo, setSueldo] = useState("")
    const [empresa, setEmpresa] = useState("")
    const [portal, setPortal] = useState("")
    const [mercadoId, setMercadoId] = useState("")
    const [modalidadId, setModalidadId] = useState("")
    const [fechaPostulacion, setFechaPostulacion] = useState("")

    async function manejarRegistro() {

        setError(null)
        setAviso("")
        setExito("")

        const listaAviso: string[] = []

        if (!puesto) { listaAviso.push("Puesto")}
        if (!empresa) { listaAviso.push("Empresa")}
        if (!fechaPostulacion) { listaAviso.push("Fecha de postulación")}

        if (listaAviso.length > 0){
            setAviso("Llena los siguientes campos: " + listaAviso.join(', '))
            return
        }

        const sueldoNumerico = parseFloat(sueldo)
        const sueldoCentavos = Math.round(sueldoNumerico * 100)

        const datosPostulacion = {
            puesto: puesto,
            sueldo_centavos: sueldoNumerico > 0 ? sueldoCentavos : null,
            empresa: empresa,
            portal: portal || null,
            mercado_id: mercadoId ? parseInt(mercadoId) : null,
            modalidad_id: modalidadId ? parseInt(modalidadId) : null,
            fecha_postulacion: fechaPostulacion
        };

        try {
            setCargando(true)

            await crearPostulacion(token, datosPostulacion)

            subirContador()

            setExito("Postulación registrada correctamente")
            
            setPuesto("")
            setSueldo("")
            setEmpresa("")
            setPortal("")
            setMercadoId("")
            setModalidadId("")
            setFechaPostulacion("")

        }
        catch (error) {
            if (error instanceof Error){
                setError(error.message)
            } else {
                setError("Ocurrió un error inesperado")
            }
        }
        finally {
            setCargando(false)
        }
    }

    // Listar mercados y modalidades para ser usados en <select>
    useEffect(() => {
        async function traerCatalogos() {
            try{
                const datosMercados = await listarMercados()
                setMercados(datosMercados)

                const datosModalidades = await listarModalidades()
                setModalidades(datosModalidades)
            }
            catch (error) {
                if (error instanceof Error) {
                    setError(error.message)
                } else {
                    setError("Ocurrió un error inesperado")
                }
            }
        }

        traerCatalogos()
    }, [])

    return(
        <div>
            {/* PUESTO */}
            <input
                type="text"
                value={puesto}
                onChange={evento => setPuesto(evento.target.value)}
                placeholder="Nombre del puesto de la vacante"/>

            {/* SUELDO */}
            <input
                type="number"
                value={sueldo}
                onChange={evento => setSueldo(evento.target.value)}
                placeholder="Sueldo de la vacante (opcional)"/>

            {/* EMPRESA */}
            <input
                type="text"
                value={empresa}
                onChange={evento => setEmpresa(evento.target.value)}
                placeholder="Empresa que publicó la vacante"/>

            {/* PORTAL */}
            <input
                type="text"
                value={portal}
                onChange={evento => setPortal(evento.target.value)}
                placeholder="Portal donde salió la vacante (opcional)"/>

            {/* LISTA DE MERCADOS */}
            <select value={mercadoId} onChange={evento => setMercadoId(evento.target.value)}>
                <option value="">Sin mercado</option>
                {mercados.map(mercado => (
                    <option key={mercado.id} value={mercado.id}>{mercado.nombre}</option>
                ))}
            </select>

            {/* LISTA DE MODALIDADES */}
            <select value={modalidadId} onChange={evento => setModalidadId(evento.target.value)}>
                <option value="">Sin modalidad</option>
                {modalidades.map(modalidad => (
                    <option key={modalidad.id} value={modalidad.id}>{modalidad.nombre}</option>
                ))}
            </select>

            {/* FECHA DE POSTULACION */}
            <input
                type="date"
                value={fechaPostulacion}
                onChange={evento => setFechaPostulacion(evento.target.value)}/>

            {/* MENSAJES */}
            {aviso && <p>{aviso}</p>}
            {cargando && <p>Espera un momento...</p>}
            {error && <p>Ocurrió un error: {error}</p>}
            {exito && <p>{exito}</p>}

            <button onClick={manejarRegistro} disabled={cargando}>
                {cargando ? "Registrando..." : "Registrar postulación"}
            </button>

        </div>
    )
}

export default NuevaPostulacion;
