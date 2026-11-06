import { useState } from "react"
import Login from "./paginas/Login"
import ListarPostulaciones from "./paginas/ListarPostulaciones"

function App() {

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
    {token ? <ListarPostulaciones token={token} removerToken={removerToken}/>: <Login alIniciarSesion={guardarToken}/>}
    </>
  )
}

export default App