from src.app import app
from flask import render_template, request, redirect, url_for, flash, session
from flask_controller import FlaskController
from src.models.productos import Producto
from src.models.categorias import Categoria


class ProductosController(FlaskController):

    @app.route('/Formulario_Producto.html', methods=['GET', 'POST'])
    def Formulario_Producto():
        categorias = Categoria.traer_categorias()

        # Detectar si se acaba de editar o crear para mostrar mensajes en el formulario
        producto_editado = session.pop('producto_editado', None)
        producto_creado = session.pop('producto_creado', None)
        producto = None

        if request.method == 'POST':
            id_producto = request.form.get('ID_Producto')
            codigo_producto = request.form.get('codigo_producto')
            producto_existente = Producto.traer_producto_por_codigo(codigo_producto)

            # --- Validación clara y separada ---
            if id_producto:  # Editando
                if producto_existente and int(id_producto) != producto_existente.ID_Producto:
                    flash('Ya existe un producto con ese código.', 'danger')
                    return redirect(url_for('Formulario_Producto'))
            else:  # Creando nuevo
                if producto_existente:
                    flash('Ya existe un producto con ese código.', 'danger')
                    return redirect(url_for('Formulario_Producto'))

            # --- Intentar guardar (crear o editar) ---
            try:
                datos_producto = {
                    'Nombre_de_producto': request.form.get('Nombre_de_producto'),
                    'Descripcion_de_producto': request.form.get('Descripcion_de_producto'),
                    'codigo_producto': codigo_producto,
                    'cantidad': int(request.form.get('cantidad')),
                    'precio': float(request.form.get('precio')),
                    'categoria_id': int(request.form.get('categoria'))
                }

                if id_producto:
                    producto = Producto.editar_producto(int(id_producto), datos_producto)
                    if producto:
                        session['producto_editado'] = True
                        return redirect(url_for('Formulario_Producto'))
                    else:
                        flash('Producto no encontrado para editar.', 'danger')
                        return redirect(url_for('Lista_productos'))

                # Si no es edición, es creación
                nuevo_producto = Producto(**datos_producto)
                Producto.crear_producto(nuevo_producto)
                session['producto_creado'] = True
                return redirect(url_for('Formulario_Producto'))

            except Exception as e:
                flash(f'Ocurrió un error al guardar el producto: {str(e)}', 'danger')

        # --- Renderizado del formulario ---
        return render_template(
            'Formulario_Producto.html',
            categorias=categorias,
            producto_editado=producto_editado,
            producto_creado=producto_creado
        )


    @app.route('/editar_producto/<int:id>', methods=['GET'])
    def editar_producto(id):
        producto = Producto.traer_producto_por_id(id)
        categorias = Categoria.traer_categorias()

        if not producto:
            flash('Producto no encontrado.', 'danger')
            return redirect(url_for('Lista_productos'))

        return render_template('Formulario_Producto.html', producto=producto, categorias=categorias)

    @app.route('/eliminar_producto/<int:id>', methods=['POST'])
    def eliminar_producto(id):
        if Producto.eliminar_producto(id):
            flash('Producto eliminado exitosamente.', 'success')
        else:
            flash('Producto no encontrado.', 'danger')

        return redirect(url_for('Lista_productos'))
    
    @app.route('/lista_productos.html')
    def Lista_productos():
        productos = Producto.traer_productos()
        return render_template('lista_productos.html', productos=productos)
    



