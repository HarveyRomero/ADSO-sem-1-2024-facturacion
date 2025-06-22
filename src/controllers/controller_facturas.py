from flask import request, render_template, redirect, url_for, flash
from datetime import datetime, date
from src.app import app 
from src.models import Session
from src.models.facturas import Factura
from src.models.detalles_factura import DetalleFactura
from src.models.TipoPago import TipoPago

@app.route('/Nueva_factura.html', methods=['GET', 'POST'])
def registrar_factura():
    if request.method == 'POST':
        session = Session()
        try:
            # 1. Crear factura
            nueva_factura = Factura(
                fecha = date.fromisoformat(request.form['fecha_factura']),
                hora = datetime.strptime(request.form['hora_factura'], '%H:%M').time(),
                valor = float(request.form['total_final']),
                ID_Cliente = int(request.form['ID_cliente']),
                ID_Usuario = int(request.form['ID_usuario'])
            )
            session.add(nueva_factura)
            session.flush()  # Para obtener el ID_factura sin hacer commit

            # 2. Crear detalles de factura
            ids_productos = request.form.getlist('producto_id[]')
            cantidades = request.form.getlist('producto_cantidad[]')
            subtotales = request.form.getlist('producto_subtotal[]')

            for i in range(len(ids_productos)):
                detalle = DetalleFactura(
                    ID_Factura = nueva_factura.ID_factura,
                    ID_Producto = int(ids_productos[i]),
                    cantidad = int(cantidades[i]),
                    subtotal = float(subtotales[i])
                )
                session.add(detalle)

            # 3. Crear tipo de pago
            pago = TipoPago(
                monto = float(request.form['valor_pagado']),
                metodoPago = request.form['metodo_pago'],
                fecha = date.today(),
                ID_Factura = nueva_factura.ID_factura
            )
            session.add(pago)

            # 4. Commit final
            session.commit()
            flash("Factura registrada correctamente.", "success")
            return redirect(url_for('Nueva_factura.html'))

        except Exception as e:
            print("Error al registrar la factura:", e)
            session.rollback()
            flash("Error al registrar la factura", "danger")
            return "Error al guardar factura", 400
        finally:
            session.close()

    return render_template('Nueva_factura.html')
