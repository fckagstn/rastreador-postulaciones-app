import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { BrowserRouter } from 'react-router-dom'
import { ProveedorAuth } from './contextos/AuthContexto.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
  <BrowserRouter>
    <ProveedorAuth>
      <App />
    </ProveedorAuth>
  </BrowserRouter>
</StrictMode>
)
