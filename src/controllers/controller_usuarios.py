from src.app import app
from flask import render_template, request, redirect, url_for, flash
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
        if request.method == 'POST':
            session = Session()
            documento_nuevo = int(request.form.get('documento_us'))
            documento_original = request.form.get('documento_original')  
            documento_original = int(documento_original) if documento_original else None

            usuario_existente = Usuario.traer_usuario_por_documento(documento_nuevo)

            if usuario_existente and (not documento_original or documento_nuevo != documento_original):
                flash('Ya existe un usuario con ese número de documento.', 'danger')
                return redirect(url_for('Registro_usuarios'))

            try:
                if documento_original:

                    usuario = session.query(Usuario).filter_by(documento_numero=documento_original).first()
                    if usuario:
                        usuario.nombre = request.form.get('Nombre_de_usu')
                        usuario.telefono = int(request.form.get('numero_celular_us'))
                        usuario.direccion = request.form.get('direccion_us')
                        usuario.email = request.form.get('correo_us')
                        usuario.usuario = request.form.get('usuario')
                        usuario.contraseña = request.form.get('Clave')
                        usuario.rol = request.form.get('rol_us')
                        usuario.documento_tipo = request.form.get('documento_tipo')
                        usuario.fecha_nacimiento = date.fromisoformat(request.form.get('fecha_nacimiento_u'))
                        usuario.ciudad = request.form.get('ciudad_us')
                        session.commit()
                        flash('Usuario actualizado correctamente', 'success')
                    else:
                        flash('Usuario no encontrado para editar.', 'danger')
                else:

                    nuevo_usuario = Usuario(
                        nombre=request.form.get('Nombre_de_usu'),
                        telefono=int(request.form.get('numero_celular_us')),
                        direccion=request.form.get('direccion_us'),
                        email=request.form.get('correo_us'),
                        usuario=request.form.get('usuario'),
                        contraseña=request.form.get('Clave'),
                        rol=request.form.get('rol_us'),
                        fecha_alta=date.today(),
                        documento_tipo=request.form.get('documento_tipo'),
                        documento_numero=documento_nuevo,
                        fecha_nacimiento=date.fromisoformat(request.form.get('fecha_nacimiento_u')),
                        ciudad=request.form.get('ciudad_us')
                    )
                    session.add(nuevo_usuario)
                    session.commit()
                    flash('Usuario creado exitosamente!', 'success')

                return redirect(url_for('Lista_usuarios'))

            except Exception as e:
                session.rollback()
                flash(f'Ocurrió un error: {str(e)}', 'danger')

        return render_template('Registro_usuarios.html')


    
    @app.route('/editar_usuario/<int:documento_numero>', methods=['GET'])
    def editar_usuario(documento_numero):
        session = Session()
        usuario = session.query(Usuario).filter_by(documento_numero=documento_numero).first()
        
        if not usuario:
            flash('Usuario no encontrado.', 'danger')
            return redirect(url_for('Lista_usuarios'))

        return render_template('Registro_usuarios.html', usuario=usuario)
    
    @app.route('/eliminar_usuario/<int:documento_numero>', methods=['POST'])
    def eliminar_usuario(documento_numero):
        session = Session()
        usuario = session.query(Usuario).filter_by(documento_numero=documento_numero).first()

        if usuario:
            session.delete(usuario)
            session.commit()
            flash('Usuario eliminado correctamente.', 'success')
        else:
            flash('Usuario no encontrado.', 'danger')

        return redirect(url_for('Lista_usuarios'))
   
    @app.route('/Lista_usuarios.html', methods=['GET'])
    def Lista_usuarios():
        usuarios = Usuario.traer_usuarios()
        return render_template('Lista_usuarios.html', usuarios=usuarios)
