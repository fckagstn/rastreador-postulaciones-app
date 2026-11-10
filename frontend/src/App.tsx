import { useState } from "react"
import Login from "./paginas/Login"
import ListarPostulaciones from "./paginas/ListarPostulaciones"
import Registro from "./paginas/Registro"
import NuevaPostulacion from "./paginas/NuevaPostulacion"
import { Routes, Route, Link, useNavigate, Navigate } from 'react-router-dom'
import RutaProtegida from "./componentes/RutaProtegida"

function App() {

  const [token, setToken] = useState(localStorage.getItem("token"))
  const [contador, setContador] = useState(0)

  const navigate = useNavigate()

  function guardarToken(token: string){
    setToken(token)
    localStorage.setItem("token", token)

    navigate("/postulaciones")
  }

  function removerToken() {
    setToken(null)
    localStorage.removeItem("token")

    navigate("/login")
  }

  function subirContador() {
    setContador((valorAnterior) => valorAnterior + 1)
  }

  return (
    <>
    <nav>
      {!token && <Link to="/login">Iniciar sesión</Link>}
      {!token && <Link to="/registro">Registrarse</Link>}
      {token && <Link to="/postulaciones">Mis postulaciones</Link>}
      {token && <Link to="/postulaciones/nueva">Nueva postulación</Link>}
      {token && <button onClick={removerToken}>Cerrar sesión</button>}
    </nav>

    <Routes>

      <Route path="/registro" element={<Registro alIniciarSesion={guardarToken}/>}/>
      <Route path="/login" element={<Login alIniciarSesion={guardarToken}/>}/>

      <Route path="/postulaciones" element={
        <RutaProtegida token={token}>
          <ListarPostulaciones token={token} contador={contador}/>
        </RutaProtegida>
      }/>

      <Route path="/postulaciones/nueva" element={
        <RutaProtegida token={token}>
          <NuevaPostulacion token={token} subirContador={subirContador}/>
        </RutaProtegida>
      }/>

      <Route path="*" element={<p>La pagina no existe</p>}/>

      <Route path="/" element={token ? <Navigate to="/postulaciones"/> : <Navigate to="/login"/>}/>

    </Routes>

    </>
  )
}

export default App