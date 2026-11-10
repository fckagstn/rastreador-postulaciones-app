import { Navigate } from "react-router-dom";
import { useAuth } from "../contextos/AuthContexto";

interface Props {
    children: React.ReactNode
}

function RutaProtegida({children}: Props){
    const {token} = useAuth()
    if (!token) {
        return <Navigate to="/login"/>
    }
    return children
}

export default RutaProtegida;