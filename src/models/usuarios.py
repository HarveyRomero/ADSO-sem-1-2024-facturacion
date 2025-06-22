from sqlalchemy import Column, Integer, String, Date, BigInteger
from sqlalchemy.orm import relationship
from src.models.base import Session, ModeloBase
from src.models import usuario_rol_enum, documento_tipo_enum


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
        
    facturas = relationship('Factura', backref='usuario', lazy=True)

    def __init__(self, nombre, telefono, direccion, email,
        usuario, contraseña, rol, fecha_alta,
        documento_tipo, documento_numero, fecha_nacimiento):
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
    def traer_usuario_por_documento(cls, numero):
        session = Session()
        return session.query(cls).filter_by(documento_numero=numero).first()

    @classmethod
    def traer_usuarios(cls):
        session = Session()
        return session.query(cls).all()

    