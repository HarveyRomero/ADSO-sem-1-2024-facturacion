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
    def crear_cliente(cls, cliente):
        session = Session()
        session.add(cliente)
        session.commit()
        session.close()
        print("Session bind:", session.bind)
        return cliente

    @classmethod
    def traer_clientes(cls):
        session = Session()
        clientes = session.query(cls).all()
        session.close()
        return clientes

    @classmethod
    def traer_cliente_por_documento(cls, documento_numero):
        session = Session()
        cliente = session.query(cls).filter_by(documento_numero=documento_numero).first()
        session.close()
        return cliente

    @classmethod
    def editar_cliente(cls, documento_original, nuevos_datos):
        session = Session()
        cliente = session.query(cls).filter_by(documento_numero=documento_original).first()
        if not cliente:
            session.close()
            return None

        cliente.nombre = nuevos_datos.get('nombre')
        cliente.telefono = nuevos_datos.get('telefono')
        cliente.direccion = nuevos_datos.get('direccion')
        cliente.email = nuevos_datos.get('email')
        cliente.documento_tipo = nuevos_datos.get('documento_tipo')
        cliente.documento_numero = nuevos_datos.get('documento_numero')
        cliente.fecha_nacimiento = nuevos_datos.get('fecha_nacimiento')
        cliente.ciudad = nuevos_datos.get('ciudad')

        session.commit()
        session.close()
        return cliente

    @classmethod
    def eliminar_cliente(cls, documento_numero):
        session = Session()
        cliente = session.query(cls).filter_by(documento_numero=documento_numero).first()
        if cliente:
            session.delete(cliente)
            session.commit()
            session.close()
            return True
        else:
            session.close()
            return False

