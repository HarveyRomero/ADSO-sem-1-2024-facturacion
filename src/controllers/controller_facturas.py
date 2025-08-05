from flask import request, render_template, flash, jsonify, make_response, session
from datetime import datetime, date
from src.app import app 
from flask_controller import FlaskController
from src.models import Session
from src.models.facturas import Factura
from src.models.detalles_factura import DetalleFactura
from src.models.TipoPago import TipoPago
from src.models.clientes import Cliente
from src.models.productos import Producto
from src.models.usuarios import Usuario
from src.models.utilidad import generar_clave_pago




class ClientesController(FlaskController):

    @app.route('/Nueva_factura.html', methods=['GET', 'POST'])
    def registrar_factura():
        if request.method == 'POST':

            print("Formulario recibido:")
            print("Cliente ID:", request.form.get('ID_Cliente'))
            print("Usuario ID:", request.form.get('ID_Usuario'))
            print("Total Final:", request.form.get('total_final'))
            print("Productos:", request.form.getlist('codigo_producto[]'))

            session = Session()
            try:
                doc_cliente = request.form['documento_numero']
                doc_usuario = request.form['documento_numerus']

                cliente = session.query(Cliente).filter_by(documento_numero=doc_cliente).first()
                usuario = session.query(Usuario).filter_by(documento_numero=doc_usuario).first()

                if not cliente or not usuario:
                    flash("Cliente o usuario no encontrado en la base de datos.", "danger")
                    return render_template('Nueva_factura.html')

                # Creo la facturilla
                nueva_factura = Factura(
                    fecha=date.today(),
                    hora=datetime.now().time(),
                    valor = float(request.form['total_final']),
                    ID_Cliente = int(request.form['ID_Cliente']),
                    ID_Usuario = int(request.form['ID_Usuario'])
                )
                session.add(nueva_factura)
                session.flush()  # Para obtener el ID_factura sin hacer commit

                # 2 detalles de facturilla
                codigos = request.form.getlist('codigo_producto[]')
                cantidades = request.form.getlist('producto_cantidad[]')
                subtotales = request.form.getlist('producto_subtotal[]')

                for i in range(len(codigos)):
                    codigo = codigos[i]
                    producto = session.query(Producto).filter_by(codigo_producto=codigo).first()

                    if not producto:
                        flash(f"Producto con código {codigo} no encontrado.", "danger")
                        return render_template('Nueva_factura.html')
                    detalle = DetalleFactura(
                        ID_Factura = nueva_factura.ID_factura,
                        ID_Producto = producto.ID_Producto,
                        cantidad = int(cantidades[i]),
                        subtotal = float(subtotales[i])
                    )
                    session.add(detalle)

                # 3 creo tipo de pago
                metodo_pago = request.form['metodo_pago']
                intermediario = request.form.get('intermediario')
                
                # Lógica condicional para las claves de los pagos
                clave_pago = None
                if metodo_pago == 'Efectivo' and intermediario:
                    clave_pago = generar_clave_pago()
                # Crear los registros de pago 
                pago = TipoPago(
                    monto = float(request.form['total_final']),
                    metodoPago = request.form['metodo_pago'],
                    intermediario_pago=intermediario if metodo_pago == 'Efectivo' else None,
                    clave_pago=clave_pago,
                    fecha = date.today(),
                    ID_Factura = nueva_factura.ID_factura
                )
                session.add(pago)

                # 4. Commit final
                session.commit()

                if metodo_pago == 'Efectivo':
                    return render_template('Nueva_factura.html', 
                            success=True,
                            mensaje="Factura generada con éxito",
                            clave_pago=clave_pago,
                            intermediario=intermediario,
                            es_efectivo=True)
                else:
                    return render_template('Nueva_factura.html',
                            success=True,
                            mensaje="Factura generada con éxito",
                            es_efectivo=False)

            except Exception as e:
                print("Error al registrar la factura:", e)
                session.rollback()
                flash("Error al registrar la factura", "danger")
                return "Error al guardar factura", 400
            finally:
                session.close()

        return render_template('Nueva_factura.html')

    @app.route('/traer_cliente_por_documento/<int:documento>', methods=['GET'])
    def traer_cliente_por_documento(documento):
        cliente = Cliente.traer_cliente_por_documento(documento)
        print("Cliente encontrado:", cliente)
        if cliente:
            return jsonify({
                'ID_Cliente': cliente.ID_Cliente,
                'nombre': cliente.nombre,
                'telefono': cliente.telefono,
                'email': cliente.email
            })
        return jsonify({'error': 'Cliente no encontrado'}), 404

    @app.route('/traer_producto_por_codigo/<codigo_producto>', methods=['GET'])
    def traer_producto_por_codigo(codigo_producto):
        producto = Producto.traer_producto_por_codigo(codigo_producto)
        print("Código recibido:", codigo_producto)
        print("Producto encontrado:", producto)
        if producto:
            return jsonify({
                'Nombre_de_producto' : producto.Nombre_de_producto,
                'precio': producto.precio
            })
        return jsonify({'error': 'Producto no encontrado'}), 404

    @app.route('/traer_usuario_por_documento/<int:documento>', methods=['GET'])
    def traer_usuario_por_documento(documento):
        usuario = Usuario.traer_usuario_por_documento(documento)
        print("Documento recibido:", documento)
        print("Usuario encontrado:", usuario)
        if usuario:
            return jsonify({
                'ID_Usuario': usuario.ID_Usuario,
                'usuario' : usuario.usuario
            })
        return jsonify({'error': 'Usuario no encontrado'}), 404

    @app.route('/Lista_facturas.html')
    def ver_facturas():
        session = Session()

        facturas = session.query(Factura).all()

        resultado = []
        for factura in facturas:
            detalles = session.query(DetalleFactura).filter_by(ID_Factura=factura.ID_factura).all()
            productos = [session.query(Producto).get(d.ID_Producto) for d in detalles]

            tipo_pago = session.query(TipoPago).filter_by(ID_Factura=factura.ID_factura).first()
            cliente = session.query(Cliente).get(factura.ID_Cliente)
            usuario = session.query(Usuario).get(factura.ID_Usuario)

            resultado.append({
                'id': factura.ID_factura,
                'fecha': factura.fecha,
                'usuario': usuario.usuario,
                'documento_tipo': cliente.documento_tipo,
                'documento_numero': cliente.documento_numero,
                'nombre_cliente': cliente.nombre,
                'productos': [p.Nombre_de_producto for p in productos],
                'total': factura.valor,
                'pago': tipo_pago.metodoPago if tipo_pago else "N/A"
            })

        session.close()
        return render_template('Lista_facturas.html', facturas=resultado)

    @app.route('/detalle_factura/<int:id_factura>')
    def detalle_factura(id_factura):
        session = Session()

        factura = session.query(Factura).get(id_factura)
        cliente = session.query(Cliente).get(factura.ID_Cliente)
        usuario = session.query(Usuario).get(factura.ID_Usuario)
        tipo_pago = session.query(TipoPago).filter_by(ID_Factura=id_factura).first()
        detalles = session.query(DetalleFactura).filter_by(ID_Factura=id_factura).all()

        for d in detalles:
                _ = d.producto.Nombre_de_producto

        session.close()

        return render_template(
            'Detalle_factura.html',
            factura=factura,
            usuario= usuario,
            cliente=cliente,
            tipo_pago=tipo_pago,
            detalles=detalles
        )





