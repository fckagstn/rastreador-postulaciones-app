import os 
from dotenv import load_dotenv

load_dotenv()

# Diccionario de variables necesarias para poder iniciar el programa
variables_obligatorias = {
    "LLAVE": os.getenv("LLAVE"),
    "DURACION_TOKEN": os.getenv("DURACION_TOKEN"),
    "FRONTEND_URL": os.getenv("FRONTEND_URL"),
    "DATABASE_URL": os.getenv("DATABASE_URL"),
    "DATABASE_URL_TEST": os.getenv("DATABASE_URL_TEST")
}

# Comprension que mete el nombre de la variable faltante en caso de que no haya valor en el diccionario
lista_variables_faltantes = [variable for variable, valor in variables_obligatorias.items() if not valor]
if lista_variables_faltantes:
    raise RuntimeError(f"Falta la variable de entorno obligatoria: {', '.join(lista_variables_faltantes)}")

llave = variables_obligatorias["LLAVE"]
duracion_token = variables_obligatorias["DURACION_TOKEN"]
frontend_url = os.getenv("FRONTEND_URL", "")
database_url = os.getenv("DATABASE_URL", "")
database_url_test = os.getenv("DATABASE_URL_TEST", "")
