from sqlalchemy import Column, Integer, String, Date, BigInteger
from sqlalchemy.orm import relationship
from src.models.base import Session, ModeloBase
from src.models import usuario_rol_enum, documento_tipo_enum
from flask import render_template, redirect, url_for, flash
from datetime import date


class Usuario(ModeloBase):
    __tablename__ = 'Usuario'
        
    ID_Usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    telefono = Column(BigInteger, nullable=False)
    direccion = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    usuario = Column(String(12), nullable=False)
    contraseña = Column(String(255), nullable=False)
    rol = Column(usuario_rol_enum, nullable=False)
    fecha_alta = Column(Date, nullable=False)
    documento_tipo = Column(documento_tipo_enum, nullable=False)
    documento_numero = Column(Integer, nullable=False, unique=True)
    fecha_nacimiento = Column(Date, nullable=False)
    ciudad = Column(String(100), nullable=False)

    facturas = relationship('Factura', backref='usuario', lazy=True)

    def __init__(self, nombre, telefono, direccion, email,
        usuario, contraseña, rol, fecha_alta,
        documento_tipo, documento_numero, fecha_nacimiento,ciudad):
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.email = email
        self.usuario = usuario
        self.contraseña = contraseña
        self.rol = rol
        self.fecha_alta = fecha_alta
        self.documento_tipo = documento_tipo
        self.documento_numero = documento_numero
        self.fecha_nacimiento = fecha_nacimiento
        self.ciudad = ciudad 

    # para verificar datos utiles en la consolita
    def __repr__(self):
        return f"<Usuario(id={self.ID_Usuario}, nombre={self.nombre}, usuario={self.usuario})>"

    @classmethod
    def crear_usuario(cls,usuario):
        session = Session()
        session.add(usuario)
        session.commit()
        return usuario
    
    @classmethod
    def traer_usuarios(cls):
        session = Session()
        return session.query(cls).all()
    
    @classmethod
    def traer_usuario_por_documento(cls, documento_numero):
        session = Session()
        return session.query(cls).filter_by(documento_numero = documento_numero).first()
    
    @classmethod
    def traer_usuario_por_id(cls, id_usuario):
        session = Session()
        usuario = session.query(cls).filter_by(ID_Usuario=id_usuario).first()
        session.close()
        return usuario
    
    @classmethod
    def editar_usuario(cls, id_usuario, nuevos_datos):
        session = Session()
        usuario= session.query(cls).filter_by(ID_Usuario=id_usuario).first()
        if not usuario:
            session.close()
            return None
        usuario.nombre = nuevos_datos.get('nombre')
        usuario.telefono = int(nuevos_datos.get('telefono'))
        usuario.direccion = nuevos_datos.get('direccion')
        usuario.email = nuevos_datos.get('email')
        usuario.usuario = nuevos_datos.get('usuario')
        usuario.contraseña = nuevos_datos.get('contraseña')
        usuario.rol = nuevos_datos.get('rol')
        usuario.documento_tipo = nuevos_datos.get('documento_tipo')
        usuario.documento_numero = nuevos_datos.get('documento_numero')
        usuario.fecha_nacimiento = nuevos_datos.get('fecha_nacimiento')
        usuario.ciudad = nuevos_datos.get('ciudad')

        session.commit()
        session.close()
        return usuario

    @classmethod
    def eliminar_usuario(cls, documento_numero):
        session = Session()
        usuario = session.query(cls).filter_by(documento_numero=documento_numero).first()
        if not usuario:
            session.close()
            return False
        session.delete(usuario)
        session.commit()
        session.close()
        return True