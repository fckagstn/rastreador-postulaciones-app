import { useState } from "react"
import Login from "./paginas/Login"
import ListarPostulaciones from "./paginas/ListarPostulaciones"

function App() {

  const [token, setToken] = useState<string | null>(null)

  function guardarToken(token: string){
    setToken(token)
  }

  return (
    <>
    {token ? <ListarPostulaciones token={token}/>: <Login alIniciarSesion={guardarToken}/>}
    </>
  )
}

export default App
