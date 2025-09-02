from sqlalchemy import Column, Integer, String, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from src.models.base import Session, ModeloBase

class Producto(ModeloBase):
    __tablename__ = 'Producto'  
        
    ID_Producto = Column(Integer, primary_key=True, autoincrement=True)
    Nombre_de_producto = Column(String(255), nullable=False)
    Descripcion_de_producto = Column(Text, nullable=False)
    codigo_producto = Column(String(9), unique=True)
    cantidad = Column(Integer, nullable=False)
    precio = Column(Numeric(10, 2), nullable=False)
        
    categoria_id = Column(Integer, ForeignKey('categoria.id'))
    categoria_rel = relationship('Categoria', back_populates='productos', lazy='joined')
    detalles = relationship('DetalleFactura', back_populates="producto")

    def __init__(self, Nombre_de_producto, Descripcion_de_producto, 
        codigo_producto, cantidad, precio, categoria_id):
        self.Nombre_de_producto = Nombre_de_producto
        self.Descripcion_de_producto = Descripcion_de_producto
        self.codigo_producto = codigo_producto
        self.cantidad = cantidad
        self.precio = precio
        self.categoria_id = categoria_id

    @classmethod
    def crear_producto(cls, producto):
        session = Session()
        session.add(producto)
        session.commit()
        session.close()
        return producto

    @classmethod
    def traer_productos(cls):
        session = Session()
        productos = session.query(cls).all()
        session.close()
        return productos

    @classmethod
    def traer_producto_por_codigo(cls, codigo_producto):
        session = Session()
        producto = session.query(cls).filter_by(codigo_producto=codigo_producto).first()
        session.close()
        return producto
    
    @classmethod
    def traer_producto_por_id(cls, id_producto):
        session = Session()
        producto = session.query(cls).filter_by(ID_Producto=id_producto).first()
        session.close()
        return producto
    
    @classmethod
    def traer_producto_por_nombre(cls, nombre):
        session = Session()
        producto = session.query(cls).filter_by(Nombre_de_producto=nombre).first()
        session.close()
        return producto

    @classmethod
    def editar_producto(cls, id_producto, nuevos_datos):
        session = Session()
        producto = session.query(cls).filter_by(ID_Producto=id_producto).first()
        if not producto:
            session.close()
            return None

        producto.Nombre_de_producto = nuevos_datos.get('Nombre_de_producto')
        producto.Descripcion_de_producto = nuevos_datos.get('Descripcion_de_producto')
        producto.codigo_producto = nuevos_datos.get('codigo_producto')
        producto.cantidad = nuevos_datos.get('cantidad')
        producto.precio = nuevos_datos.get('precio')
        producto.categoria_id = nuevos_datos.get('categoria_id')

        session.commit()
        session.close()
        return producto

    @classmethod
    def eliminar_producto(cls, id_producto):
        session = Session()
        producto = session.query(cls).filter_by(ID_Producto=id_producto).first()
        if not producto:
            session.close()
            return False
        session.delete(producto)
        session.commit()
        session.close()
        return True
