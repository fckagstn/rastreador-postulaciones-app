from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse                   # Para responder en formato JSON a cualquier error
from fastapi.middleware.cors import CORSMiddleware           # Para habilitar el intercambio de recursos de origen cruzado   
import logging                                               # Para registrar eventos del programa
import uuid           
import rastreador.rutas.cuentas as cuentas  
import rastreador.rutas.postulaciones as postulaciones

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",     # Formato de como va a arrojar los mensajes: fecha y hora | nivel de mensaje | nombre del registrador | contenido que mande
    force=True
)

logger = logging.getLogger(__name__)

app = FastAPI()

origins = [
    "http://localhost:5173",        # URL del Frontend
]

@app.exception_handler(RequestValidationError)
def manejador_validaciones(request, exc):       # Parametros: 'request' lo que manda el cliente, 'exc' el error que registra la app
    lista_errores = []
    for error in exc.errors():
        loc = error["loc"]          # Extraer la ubicación del error
        msg = error["msg"]          # Mensaje explicativo
        if "body" in loc:               # Si el error esta en el cuerpo de la petición...
            lista_errores.append(f"Error en el campo {loc[-1]}: {msg}")         # Guardar el mensaje explicando que fallo y en que campo 
        else:
            lista_errores.append("El identificador debe ser un numero entero")      # Si no esta en el cuerpo, se asume que esta en en los parametros de la URL

    return JSONResponse(status_code=422, content={"detail": " | ".join(lista_errores)})

@app.exception_handler(Exception)
def manejador_error_servidor(request, exc):
    clave = str(uuid.uuid4())
    # Registrar el error con su clave en el logger y devolver al usuario la clave del error y un mensaje generico
    logger.error("Ocurrio un error interno en el servidor con la clave %s", clave, exc_info=exc)   

    return JSONResponse(
        status_code=500, content={
            "detail": "Ocurrio un error en el servidor. Trabajaremos para solucionarlo pronto",
            "id_error": clave
        }
    )

# Registrar el Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Registrar los routers de cuentas y postulaciones
app.include_router(cuentas.router)
app.include_router(postulaciones.router)