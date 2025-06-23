from src.app import app
from flask import render_template, request, redirect, url_for, flash
from flask_controller import FlaskController
from src.models import Session
from src.models.clientes import Cliente

class ClientesController(FlaskController):
    @app.route('/Clientes.html', methods=['GET', 'POST'])
    def registrar_cliente():
        session = Session()

        if request.method == 'POST':
            documento_nuevo = int(request.form.get('documento_numero'))
            documento_original = request.form.get('documento_original')
            documento_original = int(documento_original) if documento_original else None

            try:
                if documento_original:
                    # Para poder editar mijo
                    cliente = session.query(Cliente).filter_by(documento_numero=documento_original).first()

                    if cliente:
                        # para ver si se esta editando algo que ya existe
                        if documento_nuevo != documento_original:
                            otro_cliente = Cliente.traer_cliente_por_documento(documento_nuevo)
                            if otro_cliente:
                                flash('Ya existe un cliente con ese número de documento.', 'danger')
                                return redirect(url_for('registrar_cliente'))

                        # se actuzalizan datos
                        cliente.nombre = request.form.get('Nombre_cliente')
                        cliente.telefono = int(request.form.get('numero_celular'))
                        cliente.direccion = request.form.get('direccion_cliente')
                        cliente.email = request.form.get('correo_cliente')
                        cliente.documento_tipo = request.form.get('documento_tipo')
                        cliente.documento_numero = documento_nuevo
                        cliente.fecha_nacimiento = request.form.get('fecha_nacimiento_clien')
                        cliente.ciudad = request.form.get('ciudad_cliente')

                        session.commit()
                        flash("Cliente actualizado exitosamente.", "success")
                        return redirect(url_for('listar_clientes'))

                    else:
                        flash('Cliente no encontrado para editar.', 'danger')
                        return redirect(url_for('listar_clientes'))

                else:
                    # para nuevo cleinte
                    cliente_existente = Cliente.traer_cliente_por_documento(documento_nuevo)
                    if cliente_existente:
                        flash('Ya existe un cliente con ese número de documento.', 'danger')
                        return redirect(url_for('registrar_cliente'))

                    nuevo_cliente = Cliente(
                        nombre=request.form.get('Nombre_cliente'),
                        telefono=int(request.form.get('numero_celular')),
                        direccion=request.form.get('direccion_cliente'),
                        email=request.form.get('correo_cliente'),
                        documento_tipo=request.form.get('documento_tipo'),
                        documento_numero=documento_nuevo,
                        fecha_nacimiento=request.form.get('fecha_nacimiento_clien'),
                        ciudad=request.form.get('ciudad_cliente')
                    )
                    session.add(nuevo_cliente)
                    session.commit()
                    flash("Cliente registrado exitosamente.", "success")
                    return redirect(url_for('registrar_cliente'))

            except Exception as e:
                session.rollback()
                flash(f"Error al registrar el cliente: {str(e)}", "danger")
            finally:
                session.close()

        return render_template('Clientes.html')



    @app.route('/editar_cliente/<int:documento_numero>', methods=['GET'])
    def editar_cliente(documento_numero):
        session = Session()
        cliente = session.query(Cliente).filter_by(documento_numero=documento_numero).first()

        if not cliente:
            flash('Cliente no encontrado.', 'danger')
            return redirect(url_for('listar_clientes'))

        return render_template('Clientes.html', cliente=cliente)

    @app.route('/Lista_clientes.html', methods=['GET'])
    def listar_clientes():
        session = Session()
        clientes = session.query(Cliente).all()
        session.close()
        return render_template('Lista_clientes.html', clientes=clientes)
    

    @app.route('/eliminar_cliente/<int:documento_numero>', methods=['POST'])
    def eliminar_cliente(documento_numero):
        session = Session()
        cliente = session.query(Cliente).filter_by(documento_numero=documento_numero).first()

        if cliente:
            try:
                session.delete(cliente)
                session.commit()
                flash('Cliente eliminado correctamente.', 'success')
            except Exception as e:
                session.rollback()
                flash(f'Error al eliminar el cliente: {str(e)}', 'danger')
        else:
            flash('Cliente no encontrado.', 'warning')

        session.close()
        return redirect(url_for('listar_clientes'))
