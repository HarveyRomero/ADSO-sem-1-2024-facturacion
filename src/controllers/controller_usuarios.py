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
    
        if request.method == 'POST':

            documento_numero = request.form.get('documento_numero')
            usuario_existente = Usuario.traer_usuario_por_documento(documento_numero)

            try:
                id_usuario = request.form.get('ID_Usuario')
                id_usuario = int(id_usuario) if id_usuario else None

                datos_usuario = {
                    'nombre': request.form.get('nombre'),
                    'telefono': int(request.form.get('telefono')),
                    'direccion': request.form.get('direccion'),
                    'email': request.form.get('email'),
                    'usuario': request.form.get('usuario'),
                    'contraseña': request.form.get('contraseña'),
                    'rol': request.form.get('rol'),
                    'fecha_alta': date.today(),
                    'documento_tipo': request.form.get('documento_tipo'),
                    'documento_numero': documento_numero,
                    'fecha_nacimiento': date.fromisoformat(request.form.get('fecha_nacimiento')),
                    'ciudad': request.form.get('ciudad')
                }
                if id_usuario:
                    if usuario_existente and int(id_usuario) != usuario_existente.ID_Usuario:
                        flash('Ya existe un usuario con ese numero de documento.', 'danger')
                        return redirect(url_for('Registro_usuarios'))
                    usuario = Usuario.editar_usuario(id_usuario, datos_usuario)

                    if usuario:
                        session['usuario_editado'] = True
                        return redirect(url_for('Registro_usuarios'))

                    else:
                        flash('Usuario no encontrado para editar.', 'danger')
                        return redirect(url_for('Lista_usuarios'))
                else:
                    if usuario_existente:
                        flash('Ya existe un usuario con ese numero de documento.', 'danger')
                        return redirect(url_for('Registro_usuarios'))

                    nuevo_usuario = Usuario(**datos_usuario)
                    Usuario.crear_usuario(nuevo_usuario)
                    session['usuario_creado'] = True

                return redirect(url_for('Registro_usuarios'))
            
            except Exception as e:
                flash(f'Ocurrió un error al guardar el producto: {str(e)}', 'danger')

        return render_template(
            'Registro_usuarios.html',
            usuario=usuario,
            usuario_editado = usuario_editado,
            usuario_creado = usuario_creado
        )

    
    @app.route('/editar_usuario/<int:documento_numero>', methods=['GET'])
    def editar_usuario(documento_numero):
        usuario = Usuario.traer_usuario_por_documento(documento_numero)
        
        if not usuario:
            flash('Usuario no encontrado.', 'danger')
            return redirect(url_for('Lista_usuarios'))

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
