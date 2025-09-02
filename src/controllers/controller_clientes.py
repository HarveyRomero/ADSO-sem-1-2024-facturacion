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

        # Obtener cliente si estamos editando
        documento_edicion = request.args.get('documento') or session.pop('editing_cliente_doc', None)
        if documento_edicion:
            cliente = Cliente.traer_cliente_por_documento(documento_edicion)

        if request.method == 'POST':
            documento_numero = request.form.get('documento_numero')
            documento_tipo = request.form.get('documento_tipo')
            nombre = request.form.get('nombre')
            telefono = request.form.get('telefono')
            email = request.form.get('email')
                
            cliente_existente = Cliente.traer_cliente_por_documento(documento_numero)

            try:
                documento_original = request.form.get('documento_original')
                 # Si yo renderize desde editar habra un docunemto original sino nadita
                documento_original = int(documento_original) if documento_original else None

                 # valido cuando estoy editando si existe o no 
                 # en base de datos otro cliente con ese numero 
                if documento_original:
                    if cliente_existente and cliente_existente.documento_numero != documento_original:
                        flash('Ya existe un cliente con ese número de documento.', 'danger')
                        # Si existe mantengo los daticos
                        return render_template(
                            'Clientes.html',
                            # renderizo y asigno los valores que estan en el reqets a cliente
                            cliente=request.form,
                            cliente_editado=False,
                            cliente_creado=False
                        )
                    
                else:  # Verifico si ya existe un clinete con ese documento
                    if cliente_existente:
                        flash('Ya existe un cliente con ese número de documento.', 'danger')
                        return render_template(
                            'Clientes.html',
                            # renderizo y asigno los valores que estan en el reqets a cliente
                            cliente=request.form,
                            cliente_editado=False,
                            cliente_creado=False
                        )

                # Guardo en variable bien sea para crear o editar.
                datos_cliente = {
                    'nombre': nombre,
                    'telefono': int(telefono) if telefono else None,
                    'direccion': request.form.get('direccion'),
                    'email': email,
                    'documento_tipo': documento_tipo,
                    'documento_numero': documento_numero,
                    'fecha_nacimiento': request.form.get('fecha_nacimiento'),
                    'ciudad': request.form.get('ciudad')
                }

                if documento_original:  
                    # uso la funcion editar enviando documento y el todos los datos
                    cliente = Cliente.editar_cliente(documento_original, datos_cliente)
                    if cliente:
                        session['cliente_editado'] = True
                        return redirect(url_for('registrar_cliente'))
                    else:
                        flash('Cliente no encontrado para editar.', 'danger')
                        return redirect(url_for('listar_clientes'))
                    
                else:  # Crear usanso la funcion crear cliente
                    nuevo_cliente = Cliente(**datos_cliente)
                    Cliente.crear_cliente(nuevo_cliente)
                    session['cliente_creado'] = True
                    return redirect(url_for('registrar_cliente'))

            except ValueError:
                flash('Error en los datos numéricos (teléfono).', 'danger')
                return render_template(
                    'Clientes.html',
                    cliente=request.form,
                    cliente_editado=False,
                    cliente_creado=False
                )
            
            except Exception as e:
                flash(f'Error al guardar el cliente: {str(e)}', 'danger')
                return render_template(
                    'Clientes.html',
                    cliente=request.form,
                    cliente_editado=False,
                    cliente_creado=False
                )
            
        return render_template(
            'Clientes.html',
            cliente=cliente, 
            # cuando renderizo cliente puede ser tres cosas
            # None, objeto Cliente o request.form
            cliente_editado=cliente_editado,
            cliente_creado=cliente_creado
        )


    @app.route('/editar_cliente/<int:documento_numero>', methods=['GET'])
    def editar_cliente(documento_numero):
        cliente = Cliente.traer_cliente_por_documento(documento_numero)

        if not cliente:
            flash('Cliente no encontrado.', 'danger')
            return redirect(url_for('listar_clientes'))
        
        session['editing_cliente_doc'] = documento_numero

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
