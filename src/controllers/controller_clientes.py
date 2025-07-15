from src.app import app
from flask import render_template, request, redirect, url_for, flash, session
from flask_controller import FlaskController
from src.models.clientes import Cliente


class ClientesController(FlaskController):
    
    @app.route('/Clientes.html', methods=['GET', 'POST'])
    def registrar_cliente():
        cliente_editado = session.pop('cliente_editado', None)
        cliente_creado = session.pop('cliente_creado', None)
        cliente = None

        if request.method == 'POST':
            documento_numero = request.form.get('documento_numero')
            cliente_existente = Cliente.traer_cliente_por_documento(documento_numero)

            try:
                documento_original = request.form.get('documento_original')
                documento_original = int(documento_original) if documento_original else None

                datos_cliente = {
                    'nombre': request.form.get('nombre'),
                    'telefono': int(request.form.get('telefono')),
                    'direccion': request.form.get('direccion'),
                    'email': request.form.get('email'),
                    'documento_tipo': request.form.get('documento_tipo'),
                    'documento_numero': documento_numero,
                    'fecha_nacimiento': request.form.get('fecha_nacimiento'),
                    'ciudad': request.form.get('ciudad')
                }

                if documento_original:
                    
                    if documento_existente := Cliente.traer_cliente_por_documento(documento_numero):
                        if documento_existente.documento_numero != documento_original:
                            flash('Ya existe un cliente con ese número de documento.', 'danger')
                            return redirect(url_for('registrar_cliente'))

                    cliente = Cliente.editar_cliente(documento_original, datos_cliente)
                    
                    if cliente:
                        session['cliente_editado'] = True
                        return redirect(url_for('registrar_cliente'))
                    
                    else:
                        flash('Cliente no encontrado para editar.', 'danger')
                        return redirect(url_for('listar_clientes'))

                else:
                    if cliente_existente:
                        flash('Ya existe un cliente con ese número de documento.', 'danger')
                        return redirect(url_for('registrar_cliente'))

                    nuevo_cliente = Cliente(**datos_cliente)
                    Cliente.crear_cliente(nuevo_cliente)
                    session['cliente_creado'] = True

                return redirect(url_for('registrar_cliente'))

            except Exception as e:
                flash(f"Error al guardar el cliente: {str(e)}", "danger")

        return render_template(
            'Clientes.html',
            cliente=cliente,
            cliente_editado=cliente_editado,
            cliente_creado=cliente_creado
        )


    @app.route('/editar_cliente/<int:documento_numero>', methods=['GET'])
    def editar_cliente(documento_numero):
        cliente = Cliente.traer_cliente_por_documento(documento_numero)

        if not cliente:
            flash('Cliente no encontrado.', 'danger')
            return redirect(url_for('listar_clientes'))

        return render_template('Clientes.html', cliente=cliente)
    

    @app.route('/Lista_clientes.html', methods=['GET'])
    def listar_clientes():
        clientes = Cliente.traer_clientes()
        return render_template('Lista_clientes.html', clientes=clientes)

    @app.route('/eliminar_cliente/<int:documento_numero>', methods=['POST'])
    def eliminar_cliente(documento_numero):
        if Cliente.eliminar_cliente(documento_numero):
            flash('Cliente eliminado correctamente.', 'success')
        else:
            flash('Cliente no encontrado.', 'warning')

        return redirect(url_for('listar_clientes'))
