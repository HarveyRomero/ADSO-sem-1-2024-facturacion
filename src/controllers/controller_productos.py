from src.app import app
from flask import render_template, request, redirect, url_for, flash
from flask_controller import FlaskController
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

            codigo_producto = (request.form.get('codigo_producto'))
            producto_existente = Producto.traer_producto_por_codigo(codigo_producto)
            if producto_existente:
                error = "Ya existe un producto con ese codigo."

            if producto_existente:
                flash('Ya existe un producto con ese codigo.', 'danger')
                return redirect(url_for('Formulario_Producto'))

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
                flash('Producto creado exitosamente!', 'success')
                return redirect(url_for('Formulario_Producto'))

            except Exception as e:
                flash(f'Ocurrió un error al crear el producto: {str(e)}', 'danger')


        return render_template('Formulario_Producto.html', categorias=categorias)

    @app.route('/lista_productos.html')
    def Lista_productos():
        productos = Producto.traer_productos()
        return render_template('lista_productos.html',productos = productos)


