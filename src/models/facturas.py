from sqlalchemy import Column, Integer, Numeric, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from src.models.base import Session, ModeloBase


class Factura(ModeloBase):
    __tablename__ = 'Factura'

    ID_factura = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    
    ID_Cliente = Column(Integer, ForeignKey('Cliente.ID_Cliente'), nullable=False)
    ID_Usuario = Column(Integer, ForeignKey('Usuario.ID_Usuario'), nullable=False)

    # Relaciones
    detalles = relationship('DetalleFactura', back_populates='factura', lazy=True)
    pagos = relationship('TipoPago', back_populates='factura', lazy=True)

    def __init__(self, fecha, hora, valor, ID_Cliente, ID_Usuario):
        self.fecha = fecha
        self.hora = hora
        self.valor = valor
        self.ID_Cliente = ID_Cliente
        self.ID_Usuario = ID_Usuario

    def __repr__(self):
        return f"<Factura(id={self.ID_factura}, cliente={self.ID_Cliente}, valor={self.valor})>"

    @classmethod
    def crear_factura(cls, factura):
        session = Session()
        session.add(factura)
        session.commit()
        return factura
    
    @classmethod
    def traer_facturas(cls):
        session = Session()
        return session.query(cls).all()