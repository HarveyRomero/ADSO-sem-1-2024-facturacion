from src.models import Session
from src.models.categorias import Categoria


def insertar_categorias_predeterminadas():
    session = Session()
    try:
        categorias = [
            "Computadoras y Accesorios", "Celulares y Accesorios", "Televisores y Audio",
            "Electrodomésticos pequeños", "Videojuegos y Consolas", "Redes y Conectividad",
            "Componentes y Repuestos", "Cámaras y Fotografía", "Baterías y Cargadores", "Otros accesorios"
        ]

        for nombre in categorias:
            if not session.query(Categoria).filter_by(nombre=nombre).first():
                session.add(Categoria(nombre=nombre))

        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error insertando categorías predeterminadas: {e}")
    finally:
        session.close()
