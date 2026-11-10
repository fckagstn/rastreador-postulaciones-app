import { useState } from "react"
import Login from "./paginas/Login"
import ListarPostulaciones from "./paginas/ListarPostulaciones"
import Registro from "./paginas/Registro"
import NuevaPostulacion from "./paginas/NuevaPostulacion"

function App() {

  const [mostrarRegistro, setMostrarRegistro] = useState(false)
  const [token, setToken] = useState(localStorage.getItem("token"))
  const [contador, setContador] = useState(0)

  function guardarToken(token: string){
    setToken(token)
    localStorage.setItem("token", token)
  }

  function removerToken() {
    setToken(null)
    localStorage.removeItem("token")
  }

  function subirContador() {
    setContador((valorAnterior) => valorAnterior + 1)
  }

  return (
    <>
    {token 
      ? <ListarPostulaciones token={token} removerToken={removerToken} contador={contador}/>
      : mostrarRegistro 
      ? <Registro alIniciarSesion={guardarToken} irALogin={() => setMostrarRegistro(false)}/>
      : <Login alIniciarSesion={guardarToken} irARegistro={() => setMostrarRegistro(true)}/>}

    {token && <NuevaPostulacion token={token} subirContador={subirContador}/>} 
    </>
  )
}

export default App