from flask import Flask
from src.models.base import engine, ModeloBase
from flask_controller import FlaskControllerRegister


# Modelos para asegurar que estén importados
import src.models.categorias
import src.models.detalles_factura
import src.models.productos
import src.models.clientes
import src.models.usuarios
import src.models.facturas
import src.models.TipoPago

from src.models.categorias import Categoria  # hace nueva importacionm limpiecita ome

# Crear tablas si no existen
ModeloBase.metadata.create_all(engine)


# inserto las categorias si es que no existen
Categoria.insertar_categorias_predeterminadas()


app = Flask(__name__)
app.secret_key = 'holapapu'

# Registrar los controladores
register_controllers = FlaskControllerRegister(app)
register_controllers.register_package('src.controllers')
from src.controllers.controller_facturas import *
from src.controllers import controller_productos



if __name__ == "__main__":
    app.run(debug=True)
