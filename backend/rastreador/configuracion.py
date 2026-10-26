import os 
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()

# Traer el puerto del .env, si no existe le damos el puerto predeterminado de PostgresSQL '5432'
db_port = os.getenv("DB_PORT", "5432")

# Diccionario de variables necesarias para poder iniciar el programa
variables_obligatorias = {
    "DB_USER": os.getenv("DB_USER"),
    "DB_PASSWORD": os.getenv("DB_PASSWORD"),
    "LLAVE": os.getenv("LLAVE")
}

# Comprension que mete el nombre de la variable faltante en caso de que no haya valor en el diccionario
lista_variables_faltantes = [variable for variable, valor in variables_obligatorias.items() if not valor]
if lista_variables_faltantes:
    raise RuntimeError(f"Falta la variable de entorno obligatoria: {', '.join(lista_variables_faltantes)}")

db_user = variables_obligatorias["DB_USER"]
db_password = variables_obligatorias["DB_PASSWORD"]
llave = variables_obligatorias["LLAVE"]

tiempo_expiracion = datetime.now(timezone.utc) + timedelta(minutes=10)     # 10 minutos de duracion por token