from datetime import datetime, date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import create_engine, ForeignKey, Date
from sqlalchemy.dialects.postgresql import TIMESTAMP
from rastreador.configuracion import db_port, db_user, db_password

# Engine que apunta a la BD rastreador
engine = create_engine(f"postgresql+psycopg://{db_user}:{db_password}@localhost:{db_port}/rastreador", echo=False)

class Base(DeclarativeBase):
    pass

# ==================TABLAS DEL ESQUEMA======================

class Empresa(Base):
    __tablename__= "empresas"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre_empresa: Mapped[str] = mapped_column(unique=True)

class Estado(Base):
    __tablename__ = "estados"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre_estado: Mapped[str] = mapped_column(unique=True)

class Portal(Base):
    __tablename__ = "portales"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre_portal: Mapped[str] = mapped_column(unique=True)

class Usuario(Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    apellidos: Mapped[str]
    correo: Mapped[str] = mapped_column(unique=True)
    contrasena_hashed: Mapped[str]

class Mercado(Base):
    __tablename__ = "mercado"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(unique=True)

class Modalidad(Base):
    __tablename__ = "modalidad"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(unique=True)

class Postulacion(Base):
    __tablename__ = "postulaciones"

    id: Mapped[int] = mapped_column(primary_key=True)
    puesto: Mapped[str]

    sueldo_centavos: Mapped[int | None]

    empresa_id: Mapped[int] = mapped_column(
        ForeignKey("empresas.id", ondelete="RESTRICT")
    )

    estado_id: Mapped[int] = mapped_column(
        ForeignKey("estados.id", ondelete="RESTRICT")
    )

    portal_id: Mapped[int | None] = mapped_column(
        ForeignKey("portales.id", ondelete="SET NULL"),
        nullable=True
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id", ondelete="CASCADE")
    )

    mercado_id: Mapped[int | None] = mapped_column(
        ForeignKey("mercado.id", ondelete="RESTRICT"),
        nullable=True
    )

    modalidad_id: Mapped[int | None] = mapped_column(
        ForeignKey("modalidad.id", ondelete="RESTRICT"),
        nullable=True
    )

    fecha_postulacion: Mapped[date] = mapped_column(Date)

class HistorialEstado(Base):
    __tablename__ = "historial_estados"
    id: Mapped[int] = mapped_column(primary_key=True)

    estado_id: Mapped[int] = mapped_column(
        ForeignKey("estados.id", ondelete="RESTRICT")
    )

    postulacion_id: Mapped[int] = mapped_column(
        ForeignKey("postulaciones.id", ondelete="CASCADE")
    )

    fecha: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True)
    )