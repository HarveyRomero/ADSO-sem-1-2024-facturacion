from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.models.base import ModeloBase
from src.models.base import Session

class Categoria(ModeloBase):
    __tablename__ = 'categoria'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    productos = relationship("Producto", back_populates="categoria_rel")

    @classmethod
    def insertar_categorias_predeterminadas(cls):
        session = Session()
        try:
            categorias = [
                "Computadoras y Accesorios", "Celulares y Accesorios", "Televisores y Audio",
                "Electrodomésticos pequeños", "Videojuegos y Consolas", "Redes y Conectividad",
                "Componentes y Repuestos", "Cámaras y Fotografía", "Baterías y Cargadores", "Otros accesorios"
            ]

            for nombre in categorias:
                if not session.query(cls).filter_by(nombre=nombre).first():
                    session.add(cls(nombre=nombre))

            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error insertando categorías predeterminadas: {e}")
        finally:
            session.close()

    @classmethod
    def traer_categorias(cls):
        session = Session()
        categorias = session.query(cls).order_by(cls.nombre).all()
        session.close()
        return categorias
    
