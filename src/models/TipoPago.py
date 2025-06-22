from sqlalchemy import Column, Integer, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.models.base import Session, ModeloBase
from src.models import metodo_pago_enum

class TipoPago(ModeloBase):
    __tablename__ = 'TipoPago'

    ID_Pago = Column(Integer, primary_key=True, autoincrement=True)
    monto = Column(Numeric(10, 2), nullable=False)
    metodoPago = Column(metodo_pago_enum, nullable=False)
    fecha = Column(Date, nullable=False)
    ID_Factura = Column(Integer, ForeignKey('Factura.ID_factura'), nullable=False)

    factura = relationship('Factura', back_populates='pagos')

    def __init__(self, monto, metodoPago, fecha, ID_Factura):
        self.monto = monto
        self.metodoPago = metodoPago
        self.fecha = fecha
        self.ID_Factura = ID_Factura

    def __repr__(self):
        return f"<TipoPago(id={self.ID_Pago}, monto={self.monto}, metodo={self.metodoPago})>"

    @classmethod
    def crear_TipoPago(cls, tipo_pago):
        session = Session()
        session.add(tipo_pago)
        session.commit()
        return tipo_pago
