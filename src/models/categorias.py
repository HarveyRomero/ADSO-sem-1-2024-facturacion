from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.models.base import ModeloBase



class Categoria(ModeloBase):
    __tablename__ = 'categoria'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)

    
    productos = relationship("Producto", back_populates="categoria_rel")


