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

        # Obtener producto si estamos editando (viene de la URL o session)
        producto_id = request.args.get('id') or session.pop('editing_product_id', None)
        producto = None
        if producto_id:
            producto = Producto.traer_producto_por_id(int(producto_id))

        if request.method == 'POST':
            id_producto = request.form.get('ID_Producto')
            codigo_producto = request.form.get('codigo_producto')
            nombre_producto = request.form.get('Nombre_de_producto')

            producto_existente = Producto.traer_producto_por_codigo(codigo_producto)
            producto_existente_nombre = Producto.traer_producto_por_nombre(nombre_producto)

            # Validación por producto y nombrecito
            if id_producto:  # Editando
                if producto_existente and int(id_producto) != producto_existente.ID_Producto:
                    flash('Ya existe un producto con ese código.', 'danger')
                    return render_template(
                        'Formulario_Producto.html',
                        categorias=categorias,
                        producto=request.form,
                        producto_editado=False,
                        producto_creado=False
                    )
                
                if producto_existente_nombre and int(id_producto) != producto_existente_nombre.ID_Producto:
                    flash('Ya existe un producto con ese nombre.', 'danger')
                    return render_template(
                        'Formulario_Producto.html',
                        categorias=categorias,
                        producto=request.form,
                        producto_editado=False,
                        producto_creado=False
                    )


            else:  # Creando nuevo
                if producto_existente:
                    flash('Ya existe un producto con ese código.', 'danger')
                    return render_template(
                        'Formulario_Producto.html',
                        categorias=categorias,
                        producto=request.form,
                        producto_editado=False,
                        producto_creado=False
                    )
                
                if producto_existente_nombre:
                    flash('Ya existe un producto con ese nombre.', 'danger')
                    return render_template(
                        'Formulario_Producto.html',
                        categorias=categorias,
                        producto=request.form,
                        producto_editado=False,
                        producto_creado=False
                    )

            # Almaceno datos para poder luego editar o crear
            try:
                datos_producto = {
                    'Nombre_de_producto': nombre_producto,
                    'Descripcion_de_producto': request.form.get('Descripcion_de_producto'),
                    'codigo_producto': codigo_producto,
                    'cantidad': int(request.form.get('cantidad')),
                    'precio': float(request.form.get('precio')),
                    'categoria_id': int(request.form.get('categoria'))
                }

                if id_producto: 
                    # editando ando envio la funcion editar id_producto y los demas datos
                    producto = Producto.editar_producto(int(id_producto), datos_producto)
                    if producto:
                        session['producto_editado'] = True
                        return redirect(url_for('Formulario_Producto'))
                    else:
                        flash('Producto no encontrado para editar.', 'danger')
                        return redirect(url_for('Lista_productos'))

                # Creacion de nunevo producto enviando datos
                nuevo_producto = Producto(**datos_producto)
                Producto.crear_producto(nuevo_producto)
                session['producto_creado'] = True
                return redirect(url_for('Formulario_Producto'))

            except Exception as e:
                flash(f'Ocurrió un error al guardar el producto: {str(e)}', 'danger')
                return render_template(
                    'Formulario_Producto.html',
                    categorias=categorias,
                    producto=request.form,
                    producto_editado=False,
                    producto_creado=False
                )

        # --- Renderizado del formulario ---
        return render_template(
            'Formulario_Producto.html',
            categorias=categorias,
            producto=producto, 
            # cuando formularo cliente puede ser tres cosas
            # Puede ser None para crear o un producto para editar o reqest para mentener datos
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
        
        session['editing_product_id'] = id

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
    



