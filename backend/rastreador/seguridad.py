import bcrypt
import jwt
from configuracion import llave
from datetime import datetime, timedelta, timezone

ALGORITMO = "HS256"

# Señuelo que usara la app por el canal lateral de tiempo 
senuelo = "senuelo123"

def hashear_contrasena(contrasena):
    byte_contrasena = contrasena.encode()                             # Codificar la contraseña a bytes
    sal = bcrypt.gensalt(rounds=12)
    hashed_contrasena = bcrypt.hashpw(byte_contrasena, sal)           # Generar el hash de la contraseña
    return hashed_contrasena.decode()                                 # Retornar el hash en cadena de texto

hash_senuelo = hashear_contrasena(senuelo)                            # Se llama la función hashear_contrasena al señuelo que sera ocupada por los endpoints despues

def verificar_contrasena(contrasena, hash_guardado):
    byte_contrasena = contrasena.encode()
    validacion = bcrypt.checkpw(byte_contrasena, hash_guardado.encode())    # Verificar si es True o False la contraseña contra el hash guardado en la BD en formato bytes
    return validacion

def crear_token(id_usuario):
    tiempo_expiracion = datetime.now(timezone.utc) + timedelta(hours=1)     # Una hora de duracion por token
    datos = {
        "sub": str(id_usuario),
        "exp": tiempo_expiracion
    }

    token = jwt.encode(datos, llave, ALGORITMO)
    return token

def leer_token(token):
    token_decode = jwt.decode(token, llave, algorithms=[ALGORITMO])        # Decodificar el token a formato str para extraer el sub
    sub = int(token_decode["sub"])
    return sub
