import { Navigate } from "react-router-dom";

interface Props {
    token: string;
    children: React.ReactNode
}

function RutaProtegida({token, children}: Props){
    if (!token) {
        return <Navigate to="/login"/>
    }
    return children
}

export default RutaProtegida;