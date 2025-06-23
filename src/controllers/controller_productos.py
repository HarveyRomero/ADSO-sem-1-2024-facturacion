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
            id_producto = request.form.get('ID_Producto')  # <- importante para saber si es edición
            codigo_producto = request.form.get('codigo_producto')

            # Buscar producto con ese código
            producto_existente = Producto.traer_producto_por_codigo(codigo_producto)

            # ⚠️ Validar si existe y no es el mismo que se está editando
            if producto_existente and (not id_producto or int(id_producto) != producto_existente.ID_Producto):
                flash('Ya existe un producto con ese código.', 'danger')
                return redirect(url_for('Formulario_Producto'))

            try:
                if id_producto:  # Modo edición
                    producto = session.query(Producto).filter_by(ID_Producto=id_producto).first()
                    if producto:
                        producto.Nombre_de_producto = request.form.get('Nombre_de_producto')
                        producto.Descripcion_de_producto = request.form.get('Descripcion_de_producto')
                        producto.codigo_producto = codigo_producto
                        producto.cantidad = int(request.form.get('cantidad'))
                        producto.precio = float(request.form.get('precio'))
                        producto.categoria_id = int(request.form.get('categoria'))
                        session.commit()
                        flash('Producto actualizado exitosamente!', 'success')
                        return redirect(url_for('Lista_productos'))
                    else:
                        flash('Producto no encontrado para editar.', 'danger')
                        return redirect(url_for('Lista_productos'))

                else:  # Modo creación
                    nuevo_producto = Producto(
                        Nombre_de_producto=request.form.get('Nombre_de_producto'),
                        Descripcion_de_producto=request.form.get('Descripcion_de_producto'),
                        codigo_producto=codigo_producto,
                        cantidad=int(request.form.get('cantidad')),
                        precio=float(request.form.get('precio')),
                        categoria_id=int(request.form.get('categoria'))
                    )
                    session.add(nuevo_producto)
                    session.commit()
                    flash('Producto creado exitosamente!', 'success')
                    return redirect(url_for('Formulario_Producto'))

            except Exception as e:
                flash(f'Ocurrió un error al guardar el producto: {str(e)}', 'danger')

        return render_template('Formulario_Producto.html', categorias=categorias)

    @app.route('/editar_producto/<int:id>', methods=['GET'])
    def editar_producto(id):
        session = Session()
        producto = session.query(Producto).filter_by(ID_Producto=id).first()
        categorias = session.query(Categoria).order_by(Categoria.nombre).all()

        if not producto:
            flash('Producto no encontrado.', 'danger')
            return redirect(url_for('Lista_productos'))

        return render_template('Formulario_Producto.html', producto=producto, categorias=categorias)

    @app.route('/eliminar_producto/<int:id>', methods=['POST'])
    def eliminar_producto(id):
        session = Session()
        producto = session.query(Producto).filter_by(ID_Producto=id).first()

        if not producto:
            flash('Producto no encontrado.', 'danger')
        else:
            try:
                session.delete(producto)
                session.commit()
                flash('Producto eliminado exitosamente.', 'success')
            except Exception as e:
                session.rollback()
                flash(f'Ocurrió un error al eliminar el producto: {str(e)}', 'danger')

        return redirect(url_for('Lista_productos'))



    @app.route('/lista_productos.html')
    def Lista_productos():
        productos = Producto.traer_productos()
        return render_template('lista_productos.html',productos = productos)


