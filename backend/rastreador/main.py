import logging                                               # Para registrar eventos del programa

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",     # Formato de como va a arrojar los mensajes: fecha y hora | nivel de mensaje | nombre del registrador | contenido que mande
    force=True
)

logger = logging.getLogger(__name__)
