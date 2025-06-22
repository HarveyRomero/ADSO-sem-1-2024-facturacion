from src.app import app
from flask import render_template, request, redirect, url_for,  flash
from flask_controller import FlaskController
from datetime import date
from src.models.usuarios import Usuario

class UsuariosController(FlaskController):
    @app.route('/Login_usuario.html', methods=['GET'])
    def Login_usuario():
        return render_template('Login_usuario.html')

    @app.route('/Registro_usuarios.html', methods=['GET', 'POST'])
    def Registro_usuarios():
        if request.method == 'POST':
            
            documento_numero = int(request.form.get('documento_us'))
            usuario_existente = Usuario.traer_usuario_por_documento(documento_numero)
            if usuario_existente:
                error = "Ya existe un usuario con ese número de documento."
            
            if usuario_existente:
                flash('Ya existe un usuario con ese número de documento.', 'danger')
                return redirect(url_for('Registro_usuarios'))

            try:
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
                    documento_numero=documento_numero,
                    fecha_nacimiento=date.fromisoformat(request.form.get('fecha_nacimiento_u'))
                )
                Usuario.crear_usuario(nuevo_usuario)
                flash('Usuario creado exitosamente!', 'success')
                return redirect(url_for('Registro_usuarios'))

            except Exception as e:
                flash(f'Ocurrió un error al crear el usuario: {str(e)}', 'danger')

        return render_template('Registro_usuarios.html')

    @app.route('/Lista_usuarios.html', methods=['GET'])
    def Lista_usuarios():
        usuarios = Usuario.traer_usuarios()
        return render_template('Lista_usuarios.html', usuarios=usuarios)
