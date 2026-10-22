CREATE TABLE empresas (
    id SERIAL NOT NULL PRIMARY KEY,
    nombre_empresa TEXT NOT NULL UNIQUE
);

CREATE TABLE estados (
    id SERIAL NOT NULL PRIMARY KEY,
    nombre_estado TEXT NOT NULL UNIQUE
);

CREATE TABLE portales (
    id SERIAL NOT NULL PRIMARY KEY,
    nombre_portal TEXT NOT NULL UNIQUE
);

CREATE TABLE usuarios (
    id SERIAL NOT NULL PRIMARY KEY,
    nombre TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    correo TEXT NOT NULL UNIQUE,
    contrasena_hashed TEXT NOT NULL
);

CREATE TABLE mercado (
    id SERIAL NOT NULL PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE
);

CREATE TABLE modalidad (
    id SERIAL NOT NULL PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE
);

CREATE TABLE postulaciones (
    id SERIAL NOT NULL PRIMARY KEY,
    puesto TEXT NOT NULL,
    sueldo_centavos INTEGER CHECK(sueldo_centavos > 0),
    empresa_id INTEGER NOT NULL REFERENCES empresas(id) ON DELETE RESTRICT,
    estado_id INTEGER NOT NULL REFERENCES estados(id) ON DELETE RESTRICT,
    portal_id INTEGER REFERENCES portales(id) ON DELETE SET NULL,
    usuario_id INTEGER NOT NULL REFERENCES  usuarios(id) ON DELETE CASCADE,
    mercado_id INTEGER REFERENCES mercado(id) ON DELETE RESTRICT,
    modalidad_id INTEGER REFERENCES modalidad(id) ON DELETE RESTRICT,
    fecha_postulacion DATE NOT NULL
);

CREATE TABLE historial_estados (
    id SERIAL NOT NULL PRIMARY KEY,
    estado_id INTEGER NOT NULL REFERENCES estados(id) ON DELETE RESTRICT,
    postulacion_id INTEGER NOT NULL REFERENCES  postulaciones(id) ON DELETE CASCADE,
    fecha TIMESTAMPTZ NOT NULL
);