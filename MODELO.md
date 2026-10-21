# Modelo de Base de Datos

## Tabla: usuarios

| Campo | Tipo | Restricciones |
|---------|---------|---------|
| id | SERIAL | PRIMARY KEY, NOT NULL |
| nombre | TEXT | NOT NULL |
| apellidos | TEXT | NOT NULL |
| correo | TEXT | NOT NULL, UNIQUE |
| contrasena_hashed | TEXT | NOT NULL |

---

## Tabla: postulaciones

| Campo | Tipo | Restricciones |
|---------|---------|---------|
| id | SERIAL | PRIMARY KEY, NOT NULL |
| puesto | TEXT | NOT NULL |
| sueldo_centavos | INTEGER | CHECK (sueldo_centavos > 0) |
| empresa_id | INTEGER | NOT NULL, FK → empresas(id) |
| estado_id | INTEGER | NOT NULL, FK → estados(id) |
| portal_id | INTEGER | FK → portales(id) |
| usuario_id | INTEGER | NOT NULL, FK → usuarios(id) |
| mercado_id | INTEGER | FK → mercado(id) |
| modalidad_id | INTEGER | FK → modalidad(id) |
| fecha_postulacion | DATE | NOT NULL |

---

## Tabla: portales

| Campo | Tipo | Restricciones |
|---------|---------|---------|
| id | SERIAL | PRIMARY KEY, NOT NULL |
| nombre_portal | TEXT | NOT NULL, UNIQUE |

---

## Tabla: estados

| Campo | Tipo | Restricciones |
|---------|---------|---------|
| id | SERIAL | PRIMARY KEY, NOT NULL |
| nombre_estado | TEXT | NOT NULL, UNIQUE |

---

## Tabla: empresas

| Campo | Tipo | Restricciones |
|---------|---------|---------|
| id | SERIAL | PRIMARY KEY, NOT NULL |
| nombre_empresa | TEXT | NOT NULL, UNIQUE |

---

## Tabla: historial_estados

| Campo | Tipo | Restricciones |
|---------|---------|---------|
| id | SERIAL | PRIMARY KEY, NOT NULL |
| estado_id | INTEGER | NOT NULL, FK → estados(id) |
| postulacion_id | INTEGER | NOT NULL, FK → postulaciones(id) |
| fecha | TIMESTAMPTZ | NOT NULL |

### Nota
Se utiliza `TIMESTAMPTZ` para almacenar fecha y hora normalizadas en UTC, permitiendo consistencia temporal cuando la aplicación es utilizada por usuarios en diferentes zonas horarias.

---

## Tabla: modalidad

| Campo | Tipo | Restricciones |
|---------|---------|---------|
| id | SERIAL | PRIMARY KEY, NOT NULL |
| nombre | TEXT | NOT NULL, UNIQUE |

---

## Tabla: mercado

| Campo | Tipo | Restricciones |
|---------|---------|---------|
| id | SERIAL | PRIMARY KEY, NOT NULL |
| nombre | TEXT | NOT NULL, UNIQUE |

---

# Relaciones

- Una **empresa** puede tener muchas **postulaciones**.
- Un **usuario** puede realizar muchas **postulaciones**.
- Una **postulación** pertenece a una sola **empresa**.
- Una **postulación** pertenece a un solo **usuario**.
- Una **postulación** tiene un **estado actual**.
- Una **postulación** puede registrar múltiples cambios en **historial_estados**.
- Una **postulación** puede estar asociada a un **portal**.
- Una **postulación** puede estar asociada a una **modalidad**.
- Una **postulación** puede estar asociada a un **mercado**.

---

# Decisiones tomadas

- Se agregó una tabla `usuarios` respecto al proyecto base, además de los catálogos `modalidad` y `mercado`. Esto permite clasificar una postulación según su modalidad (presencial, híbrida o remota) y según el mercado de la empresa (local, nacional, nearshore, offshore, entre otros).

- Los sueldos se almacenan en centavos utilizando un `INTEGER`. De esta forma se evitan posibles problemas de precisión al intercambiar datos entre PostgreSQL, Python, JSON y React. El valor permanece exacto durante todo el flujo de datos y únicamente se convierte a pesos al momento de mostrarse al usuario.

- Se agregó la tabla `historial_estados` para conservar la trazabilidad de cada postulación. Gracias a ella es posible conocer cuándo cambió de estado una postulación y reconstruir toda su evolución en el tiempo.

- Las empresas se manejan de forma global y no por usuario. Esto evita duplicar información cuando distintos usuarios se postulan a la misma empresa. Como medida para reducir inconsistencias en nombres similares o escritos de forma diferente, el frontend mostrará las empresas ya registradas mediante listas desplegables.

- Los estados se modelaron mediante una tabla catálogo en lugar de un `CHECK`. Esto facilita agregar o  modificar estados sin necesidad de alterar restricciones complejas de la base de datos. El costo es la necesidad de realizar consultas con JOIN, a cambio de una mayor flexibilidad.

- `usuario_id` va donde esta el dato que le pertenece a alguien. A través de una postulación es posible identificar al usuario y acceder indirectamente al resto de la información relacionada.

- Se descartó la restricción que impedía registrar más de una postulación para la misma empresa. Un usuario puede postularse varias veces a una empresa para puestos distintos o en momentos diferentes, por lo que dicha restricción no representaba correctamente la realidad del negocio.

- El estado actual de la postulación se conserva en `postulaciones.estado_id` y, al mismo tiempo, cada cambio queda registrado en `historial_estados`. Esta es una desnormalización deliberada que permite consultar rápidamente el estado actual sin recalcularlo desde el historial. Para evitar inconsistencias, ambas actualizaciones deberán realizarse dentro de la misma transacción.