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