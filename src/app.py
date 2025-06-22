from flask import Flask
from src.models.base import engine, ModeloBase
from flask_controller import FlaskControllerRegister
from src.models.detalles_factura import DetalleFactura


import src.models.categorias
import src.models.detalles_factura
import src.models.productos
import src.models.clientes
import src.models.usuarios
import src.models.facturas
import src.models.TipoPago


ModeloBase.metadata.create_all(engine)

from src.controllers.controller_categorias import insertar_categorias_predeterminadas

insertar_categorias_predeterminadas()


app = Flask(__name__)
app.secret_key = 'holapapu'

insertar_categorias_predeterminadas()

register_controllers = FlaskControllerRegister(app)
register_controllers.register_package('src.controllers')

if __name__ == "__main__":
    app.run(debug=True)

