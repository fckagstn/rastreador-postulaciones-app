import { useState } from "react"
import Login from "./paginas/Login"
import ListarPostulaciones from "./paginas/ListarPostulaciones"
import Registro from "./paginas/Registro"

function App() {

  const [mostrarRegistro, setMostrarRegistro] = useState(false)
  const [token, setToken] = useState(localStorage.getItem("token"))

  function guardarToken(token: string){
    setToken(token)
    localStorage.setItem("token", token)
  }

  function removerToken() {
    setToken(null)
    localStorage.removeItem("token")
  }

  return (
    <>
    {token 
      ? <ListarPostulaciones token={token} removerToken={removerToken}/>
      : mostrarRegistro 
      ? <Registro alIniciarSesion={guardarToken} irALogin={() => setMostrarRegistro(false)}/>
      : <Login alIniciarSesion={guardarToken} irARegistro={() => setMostrarRegistro(true)}/>} 
    </>
  )
}

export default App