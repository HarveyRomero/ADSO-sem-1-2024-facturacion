from sqlalchemy import Column, Integer, String, Date, BigInteger
from sqlalchemy.orm import relationship
from src.models.base import Session, ModeloBase
from src.models import documento_tipo_enum


class Cliente(ModeloBase):
    __tablename__ = 'Cliente'
        
    ID_Cliente = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    telefono = Column(BigInteger, nullable=False)
    direccion = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    documento_tipo = Column(documento_tipo_enum, nullable=False)
    documento_numero = Column(Integer, nullable=False, unique=True)
    fecha_nacimiento = Column(Date, nullable=False)
    ciudad = Column(String(100), nullable=False)
        
    facturas = relationship('Factura', backref='cliente', lazy=True)


    def __init__(self, nombre, telefono, direccion, email,
    documento_tipo, documento_numero, fecha_nacimiento, ciudad):
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.email = email
        self.documento_tipo = documento_tipo
        self.documento_numero = documento_numero 
        self.fecha_nacimiento = fecha_nacimiento
        self.ciudad = ciudad

    @classmethod
    def crear_cliente(cls,cliente):
        session = Session()
        session.add(cliente)
        session.commit()
        return cliente
    
    @classmethod
    def traer_clientes(cls):
        session = Session()
        return session.query(cls).all()
    
    @classmethod
    def traer_cliente_por_documento(cls, documento_numero):
        session = Session()
        cliente = session.query(cls).filter_by(documento_numero=documento_numero).first()
        session.close()
        return cliente