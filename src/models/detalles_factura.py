from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from src.models.base import Session, ModeloBase


class DetalleFactura(ModeloBase):
    __tablename__ = 'DetalleFactura'

    ID_Detalle = Column(Integer, primary_key=True, autoincrement=True)
    ID_Factura = Column(Integer, ForeignKey('Factura.ID_factura'), nullable=False)
    ID_Producto = Column(Integer, ForeignKey('Producto.ID_Producto'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)

    # Relaciones recomendadas (opcional pero útil)
    factura = relationship('Factura', back_populates='detalles')
    producto = relationship('Producto', back_populates="detalles")
    

    def __init__(self, ID_Factura, ID_Producto, cantidad, subtotal):
        self.ID_Factura = ID_Factura
        self.ID_Producto = ID_Producto
        self.cantidad = cantidad
        self.subtotal = subtotal

    def __repr__(self):
        return f"<DetalleFactura(id={self.ID_Detalle}, factura={self.ID_Factura}, producto={self.ID_Producto}, cantidad={self.cantidad})>"

    @classmethod
    def crear_detalle_factura(cls, detalle):
        session = Session()
        session.add(detalle)
        session.commit()
        return detalle
    
    @classmethod
    def traer_detalles(cls):
        session = Session()
        return session.query(cls).all()