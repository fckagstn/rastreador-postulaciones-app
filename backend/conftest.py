import pytest
import uuid
from fastapi.testclient import TestClient
from rastreador.main import app

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
