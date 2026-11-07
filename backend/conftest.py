import pytest
import uuid
from fastapi.testclient import TestClient
from rastreador.main import app
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from rastreador.configuracion import database_url_test
from rastreador.dependencias import obtener_sesion
from rastreador.modelos_mapeados import Base, Estado, Mercado, Modalidad

if not database_url_test: 
    raise RuntimeError("Falta la conexión para la BD de pruebas")

# Crear un cliente para pruebas
@pytest.fixture()
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
        "correo": f"{correo}@test.com",
        "contrasena": contrasena
    })

    datos = {
        "correo": f"{correo}@test.com",
        "contrasena": contrasena
    }

    yield datos

# Crear la conexion, se usa una BD aparte para test para evitar tocar los datos de la BD original
engine_test = create_engine(database_url_test, echo=False)

def obtener_session_test():
    with Session(engine_test) as session:
        yield session

@pytest.fixture(autouse=True)
def crear_db_test_y_registrar_session():
    Base.metadata.create_all(engine_test)

    # Sembrar los datos de los catalogos para que no truenen las pruebas si los necesitan
    with Session(engine_test) as session:
        estados = [
            Estado(nombre_estado="postulado"),
            Estado(nombre_estado="rechazado"),
            Estado(nombre_estado="entrevista"),
            Estado(nombre_estado="oferta")
        ]

        mercados = [
            Mercado(nombre="local"),
            Mercado(nombre="nacional"),
            Mercado(nombre="nearshore"),
            Mercado(nombre="offshore")
        ]

        modalidades = [
            Modalidad(nombre="presencial"),
            Modalidad(nombre="remoto"),
            Modalidad(nombre="híbrido")
        ]

        session.add_all(estados)
        session.add_all(mercados)
        session.add_all(modalidades)
        session.commit()

    app.dependency_overrides[obtener_sesion] = obtener_session_test
    yield

    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine_test)