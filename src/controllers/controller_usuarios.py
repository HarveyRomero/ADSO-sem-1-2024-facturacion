from src.app import app
from flask import render_template, request, redirect, url_for, flash, session
from flask_controller import FlaskController
from datetime import date
from src.models.usuarios import Usuario
from src.models import Session

class UsuariosController(FlaskController):
    @app.route('/Login_usuario.html', methods=['GET'])
    def Login_usuario():
        return render_template('Login_usuario.html')

    @app.route('/Registro_usuarios.html', methods=['GET', 'POST'])
    def Registro_usuarios():

        usuario_editado = session.pop('usuario_editado', None)
        usuario_creado = session.pop('usuario_creado', None)
        usuario = None

 # Obtener cliente si estamos editando
        id_edicion = request.args.get('id') or session.pop('editing_usuario_id', None)
        if id_edicion:
            usuario = Usuario.traer_usuario_por_id(int(id_edicion))

        if request.method == 'POST':
            # Obtener todos los campos
            documento_numero = request.form.get('documento_numero')
            nombre = request.form.get('nombre')
            telefono = request.form.get('telefono')
            email = request.form.get('email')
            usuario_name = request.form.get('usuario')
            contraseña = request.form.get('contraseña')
            rol = request.form.get('rol')
            documento_tipo = request.form.get('documento_tipo')
            fecha_nacimiento = request.form.get('fecha_nacimiento')
            ciudad = request.form.get('ciudad')
            direccion = request.form.get('direccion')

            usuario_existente = Usuario.traer_usuario_por_documento(documento_numero)

            try:
                id_usuario = request.form.get('ID_Usuario')
                # Si yo renderize desde editar habra un Id original  sino nadita
                id_usuario = int(id_usuario) if id_usuario else None

                 # valido cuando estoy editando si existe o no 
                 # en base de datos otro usurio con ese id 
                if id_usuario:  # Editando
                    if usuario_existente and usuario_existente.ID_Usuario != id_usuario:
                        flash('Ya existe un usuario con ese número de documento.', 'danger')
                        # Mantener todos los datos del formulario
                        return render_template(
                            'Registro_usuarios.html',
                            usuario=request.form,
                            usuario_editado=False,
                            usuario_creado=False
                        )

                else:  # Verifico si ya existe un usurio con ese ID
                    if usuario_existente:
                        flash('Ya existe un usuario con ese número de documento.', 'danger')
                        return render_template(
                            'Registro_usuarios.html',
                            # renderizo y asigno los valores que estan en el reqets a usuario
                            usuario=request.form,
                            usuario_editado=False,
                            usuario_creado=False
                        )

                # Guardo en variable bien sea para crear o editar.
                datos_usuario = {
                    'nombre': nombre,
                    'telefono': int(telefono) if telefono else None,
                    'direccion': direccion,
                    'email': email,
                    'usuario': usuario_name,
                    'contraseña': contraseña,
                    'rol': rol,
                    'fecha_alta': date.today(),
                    'documento_tipo': documento_tipo,
                    'documento_numero': documento_numero,
                    'fecha_nacimiento': date.fromisoformat(fecha_nacimiento) if fecha_nacimiento else None,
                    'ciudad': ciudad
                }

                if id_usuario:
                    # uso la funcion editar enviando id y el todos los datos
                    usuario = Usuario.editar_usuario(id_usuario, datos_usuario)
                    if usuario:
                        session['usuario_editado'] = True
                        return redirect(url_for('Registro_usuarios'))
                    else:
                        flash('Usuario no encontrado para editar.', 'danger')
                        return redirect(url_for('Lista_usuarios'))

                else:   # Crear usanso la funcion crear usuario
                    nuevo_usuario = Usuario(**datos_usuario)
                    Usuario.crear_usuario(nuevo_usuario)
                    session['usuario_creado'] = True
                    return redirect(url_for('Registro_usuarios'))
                
            except Exception as e:
                flash(f'Ocurrió un error al guardar el usuario: {str(e)}', 'danger')
                return render_template(
                    'Registro_usuarios.html',
                    usuario=request.form,
                    usuario_editado=False,
                    usuario_creado=False
                )
                # --- RENDERIZADO DEL FORMULARIO (GET) ---
        return render_template(
            'Registro_usuarios.html',
            usuario=usuario,  # Puede ser None, objeto Usuario o request.form
            usuario_editado=usuario_editado,
            usuario_creado=usuario_creado
        )
        
    
    @app.route('/editar_usuario/<int:id_usuario>', methods=['GET'])
    def editar_usuario(id_usuario):
        usuario = Usuario.traer_usuario_por_id(id_usuario)
        
        if not usuario:
            flash('Usuario no encontrado.', 'danger')
            return redirect(url_for('Lista_usuarios'))

        # Guardar ID en session para persistir en caso de error POST
        session['editing_usuario_id'] = id_usuario
        
        return render_template('Registro_usuarios.html', usuario=usuario)

    
    @app.route('/eliminar_usuario/<int:documento_numero>', methods=['POST'])
    def eliminar_usuario(documento_numero):
 
        if Usuario.eliminar_usuario(documento_numero):
            flash('Usuario eliminado correctamente.', 'success')
        else:
            flash('Usuario no encontrado.', 'danger')

        return redirect(url_for('Lista_usuarios'))
    
   
    @app.route('/Lista_usuarios.html', methods=['GET'])
    def Lista_usuarios():
        usuarios = Usuario.traer_usuarios()
        return render_template('Lista_usuarios.html', usuarios=usuarios)
