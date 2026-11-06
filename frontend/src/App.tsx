import { useState } from "react"
import Login from "./paginas/Login"

function App() {

  const [token, setToken] = useState<string | null>(null)

  function guardarToken(token: string){
    setToken(token)
  }

  return (
    <>
    {token ? <p>Sesión iniciada con éxito</p>: <Login alIniciarSesion={guardarToken}/>}
    </>
  )
}

export default App
