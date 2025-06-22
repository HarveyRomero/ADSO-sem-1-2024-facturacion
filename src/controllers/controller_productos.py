from src.app import app
from flask import render_template, request, redirect, url_for
from flask_controller import FlaskController
from src.models import Session
from src.models.productos import Producto
from src.models.categorias import Categoria


class ProductosController(FlaskController):
    @app.route('/Formulario_Producto.html', methods=['GET', 'POST'])
    def Formulario_Producto():
        session = Session()
        categorias = session.query(Categoria).order_by(Categoria.nombre).all()
        if request.method == 'POST':
            print(request.form) 
            try:
                nuevo_producto = Producto(
                Nombre_de_producto=request.form.get('Nombre_de_producto'),
                Descripcion_de_producto=request.form.get('Descripcion_de_producto'),
                codigo_producto=request.form.get('codigo_producto'),
                cantidad=int(request.form.get('cantidad')),
                precio=float(request.form.get('precio')),
                categoria_id=int(request.form.get('categoria'))
                )
                session.add(nuevo_producto)
                session.commit()
                return redirect(url_for('Formulario_Producto'))

            except Exception as e:
                print("Error al guardar producto:", e)

        return render_template('Formulario_Producto.html', categorias=categorias)

    @app.route('/lista_productos.html')
    def Lista_productos():
        productos = Producto.traer_productos()
        return render_template('lista_productos.html',productos = productos)


