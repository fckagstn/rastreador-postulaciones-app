import { useState } from "react"
import Login from "./paginas/Login"
import ListarPostulaciones from "./paginas/ListarPostulaciones"
import Registro from "./paginas/Registro"
import NuevaPostulacion from "./paginas/NuevaPostulacion"
import { Routes, Route, Link, Navigate } from 'react-router-dom'
import RutaProtegida from "./componentes/RutaProtegida"
import { useAuth } from "./contextos/AuthContexto"

function App() {

  const [contador, setContador] = useState(0)
  const { token, removerToken } = useAuth()

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

      <Route path="/registro" element={<Registro/>}/>
      <Route path="/login" element={<Login />}/>

      <Route path="/postulaciones" element={
        <RutaProtegida>
          <ListarPostulaciones contador={contador}/>
        </RutaProtegida>
      }/>

      <Route path="/postulaciones/nueva" element={
        <RutaProtegida>
          <NuevaPostulacion subirContador={subirContador}/>
        </RutaProtegida>
      }/>

      <Route path="*" element={<p>La pagina no existe</p>}/>

      <Route path="/" element={token ? <Navigate to="/postulaciones"/> : <Navigate to="/login"/>}/>

    </Routes>

    </>
  )
}

export default App