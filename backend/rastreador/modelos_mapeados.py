from datetime import datetime, date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
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
    postulaciones: Mapped[list["Postulacion"]] = relationship(back_populates="empresa")

class Estado(Base):
    __tablename__ = "estados"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre_estado: Mapped[str] = mapped_column(unique=True)
    postulaciones: Mapped[list["Postulacion"]] = relationship(back_populates="estado")
    historial: Mapped[list["HistorialEstado"]] = relationship(back_populates="estado")

class Portal(Base):
    __tablename__ = "portales"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre_portal: Mapped[str] = mapped_column(unique=True)
    postulaciones: Mapped[list["Postulacion"]] = relationship(back_populates="portal")

class Usuario(Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    apellidos: Mapped[str]
    correo: Mapped[str] = mapped_column(unique=True)
    contrasena_hashed: Mapped[str]
    postulaciones: Mapped[list["Postulacion"]] = relationship(back_populates="usuario")

class Mercado(Base):
    __tablename__ = "mercado"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(unique=True)
    postulaciones: Mapped[list["Postulacion"]] = relationship(back_populates="mercado")

class Modalidad(Base):
    __tablename__ = "modalidad"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(unique=True)
    postulaciones: Mapped[list["Postulacion"]] = relationship(back_populates="modalidad")

class Postulacion(Base):
    __tablename__ = "postulaciones"

    id: Mapped[int] = mapped_column(primary_key=True)
    puesto: Mapped[str]

    sueldo_centavos: Mapped[int | None]

    # ==========LLAVES FORANEAS==============
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

    # ==========RELACIONES=============
    usuario: Mapped["Usuario"] = relationship(back_populates="postulaciones")
    empresa: Mapped["Empresa"] = relationship(back_populates="postulaciones")
    estado: Mapped["Estado"] = relationship(back_populates="postulaciones")
    portal: Mapped["Portal"] = relationship(back_populates="postulaciones")
    mercado: Mapped["Mercado"] = relationship(back_populates="postulaciones")
    modalidad: Mapped["Modalidad"] = relationship(back_populates="postulaciones")
    historial: Mapped[list["HistorialEstado"]] = relationship(back_populates="postulacion")

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

    postulacion: Mapped["Postulacion"] = relationship(back_populates="historial")
    estado: Mapped["Estado"] = relationship(back_populates="historial")