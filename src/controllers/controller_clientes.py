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

            documento_numero = int(request.form.get('documento_numero'))
            usuario_existente = Cliente.traer_cliente_por_documento(documento_numero)
            if usuario_existente:
                error = "Ya existe un cliente con ese número de documento."

            if usuario_existente:
                flash('Ya existe un cliente con ese número de documento.', 'danger')
                return redirect(url_for('registrar_cliente'))
            
            try:
                nuevo_cliente = Cliente(
                    nombre=request.form.get('Nombre_cliente'),
                    telefono=int(request.form.get('numero_celular')),
                    direccion=request.form.get('direccion_cliente'),
                    email=request.form.get('correo_cliente'),
                    documento_tipo=request.form.get('documento_text'),
                    documento_numero=int(request.form.get('documento_numero')),
                    fecha_nacimiento=request.form.get('fecha_nacimiento_clien'),
                    ciudad=request.form.get('ciudad_cliente')
                )
                session.add(nuevo_cliente)
                session.commit()

                flash("Cliente registrado exitosamente.", "success")
                return redirect(url_for('registrar_cliente'))

            except Exception as e:
                flash(f"Error al registrar el cliente: {str(e)}", "danger")
            finally:
                session.close()

        return render_template('Clientes.html')

    @app.route('/Lista_clientes.html', methods=['GET'])
    def listar_clientes():
        session = Session()
        clientes = session.query(Cliente).all()
        session.close()
        return render_template('Lista_clientes.html', clientes=clientes)
