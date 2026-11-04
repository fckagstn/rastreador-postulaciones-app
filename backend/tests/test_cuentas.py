def test_registrar_usuario_nuevo_responde_201(cliente):
    respuesta = cliente.post("/usuarios", json={
        "nombre": "usuario",
        "apellidos": "pruebas",
        "correo": "usuario@test.com",
        "contrasena": "contrasena123"
    })
    
    assert respuesta.status_code == 201

def test_registrar_correo_duplicado_responde_409(cliente):
    cliente.post("/usuarios", json={
        "nombre": "usuario",
        "apellidos": "pruebas",
        "correo": "usuario@test.com",
        "contrasena": "contrasena123"
    })

    respuesta_duplicada = cliente.post("/usuarios", json={
        "nombre": "usuario",
        "apellidos": "pruebas",
        "correo": "usuario@test.com",
        "contrasena": "contrasena123"
    })

    assert respuesta_duplicada.status_code == 409

def test_login_credenciales_correctas_responde_200(cliente, usuario_temporal):
    respuesta = cliente.post("/login", json={
        "correo": usuario_temporal["correo"],
        "contrasena": usuario_temporal["contrasena"]
    })
    assert respuesta.status_code == 200

def test_login_credenciales_incorrectas_responde_401(cliente):
    respuesta = cliente.post("/login", json={
        "correo": "inexistente@test.com",
        "contrasena": "contrasena_test"
    })
    assert respuesta.status_code == 401

def test_traer_perfil_con_token_responde_200(cliente, token):
    respuesta = cliente.get("/perfil", headers={"Authorization": f"Bearer {token}"})
    assert respuesta.status_code == 200

def test_traer_perfil_sin_token_responde_401(cliente):
    respuesta = cliente.get("/perfil")
    assert respuesta.status_code == 401