from flask import Flask, render_template

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Login_usuario.html')
def Login_usuario():
    return render_template('Login_usuario.html')

@app.route('/Registro_usuarios.html')
def Registro_usuarios():
    return render_template('Registro_usuarios.html')

@app.route('/Lista_usuarios.html')
def Lista_usuarios():
    return render_template('Lista_usuarios.html')

@app.route('/Formulario_Producto.html')
def Formulario_Producto():
    return render_template('Formulario_Producto.html')

@app.route('/Lista_productos.html')
def Lista_productos():
    return render_template('Lista_productos.html')

@app.route('/Clientes.html')
def Clientes():
    return render_template('Clientes.html')

@app.route('/Lista_clientes.html')
def Lista_clientes():
    return render_template('Lista_clientes.html')

@app.route('/Nueva_factura.html')
def Nueva_factura():
    return render_template('Nueva_factura.html')

@app.route('/Lista_facturas.html')
def Lista_facturas():
    return render_template('Lista_facturas.html')


