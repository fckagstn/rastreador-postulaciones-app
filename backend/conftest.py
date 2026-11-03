import pytest
import uuid
from fastapi.testclient import TestClient
from rastreador.main import app
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from rastreador.configuracion import db_password, db_port, db_user

# Crear un cliente para pruebas
@pytest.fixture
def cliente():
    return TestClient(app)

@pytest.fixture
def token(cliente, usuario_temporal):
    login = cliente.post("/login", json={
        "correo": usuario_temporal["correo"],
        "contrasena": usuario_temporal["contrasena"]
    })

    datos_login = login.json()
    token = datos_login["access_token"]
    return token

# Registrar un usuario temporal para usar durante las pruebas 
@pytest.fixture
def usuario_temporal(cliente):
    nombre = str(uuid.uuid4())
    apellidos = str(uuid.uuid4())
    correo = str(uuid.uuid4())
    contrasena = str(uuid.uuid4())

    cliente.post("/usuarios", json={
        "nombre": nombre,
        "apellidos": apellidos,
        "correo": correo,
        "contrasena": contrasena
    })

    datos = {
        "correo": correo,
        "contrasena": contrasena
    }

    yield datos

# Crear la conexion, se usa una BD aparte para test para evitar tocar los datos de la BD original
engine_test = create_engine(f"postgresql+psycopg://{db_user}:{db_password}@localhost:{db_port}/rastreador_test", echo=False)

def obtener_session_test():
    with Session(engine_test) as session:
        yield session