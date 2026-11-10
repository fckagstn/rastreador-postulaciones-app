import { createContext ,useState, useContext } from "react"
import {  useNavigate } from "react-router-dom"
import { type ReactNode } from "react";

interface ValorAuth {
    token: string | null;
    guardarToken: (token: string) => void;
    removerToken: () => void;
}

const AuthContexto = createContext<ValorAuth | null>(null);

export function ProveedorAuth({ children }: { children: ReactNode }) {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const navigate = useNavigate();

  function guardarToken(token: string) {
    setToken(token);
    localStorage.setItem("token", token);
    navigate("/postulaciones");
  }

  function removerToken() {
    setToken(null);
    localStorage.removeItem("token");
    navigate("/login");
  }

  return (
    <AuthContexto.Provider value={{ token, guardarToken, removerToken }}>
      {children}
    </AuthContexto.Provider>
  );
}

export function useAuth() {
  const valor = useContext(AuthContexto);
  if (valor === null) {
    throw new Error("useAuth debe usarse dentro de ProveedorAuth");
  }
  return valor;
}