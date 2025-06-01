from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String, Text, Numeric, Date, Time, ForeignKey 
from sqlalchemy import Enum
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import pymysql
from datetime import date

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)

engine = create_engine("mysql+pymysql://root@localhost/basepython1?charset=utf8mb4")
connection = engine.connect()


Session = sessionmaker(bind=engine)

ModeloBase = declarative_base()
ModeloBase.metadata.bind = engine


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Login_usuario.html')
def Login_usuario():
    return render_template('Login_usuario.html')

@app.route('/Registro_usuarios.html', methods=['GET', 'POST'])
def Registro_usuarios():
    session = Session()
    if request.method == 'POST':
        print("Formulario recibido")
        print(request.form) 
        nombre = request.form.get('Nombre_de_usu')
        documento_tipo = request.form.get('documento_tipo')
        documento_numero = int(request.form.get('documento_us'))
        fecha_nacimiento = date.fromisoformat(request.form.get('fecha_nacimiento_u'))
        email = request.form.get('correo_us')
        direccion = request.form.get('direccion_us')
        telefono = int(request.form.get('numero_celular_us'))
        usuario = request.form.get('usuario')
        contraseña = request.form.get('Clave')
        rol = request.form.get('rol_us')

        nuevo_usuario = Usuario(
            nombre=nombre,
            telefono=telefono,
            direccion=direccion,
            email=email,
            usuario=usuario,
            contraseña=contraseña,
            rol=rol,
            fecha_alta=date.today(),
            documento_tipo=documento_tipo,
            documento_numero=documento_numero,
            fecha_nacimiento=fecha_nacimiento
        )

        session.add(nuevo_usuario)
        session.commit()

        return redirect(url_for('Registro_usuarios'))

    return render_template('Registro_usuarios.html')


@app.route('/Lista_usuarios.html')
def Lista_usuarios():
    return render_template('Lista_usuarios.html')

@app.route('/Formulario_Producto.html', methods=['GET', 'POST'])
def Formulario_Producto():
    session = Session()
    
    if request.method == 'POST':
        ID_Producto = request.form.get('ID_Producto')
        Nombre_de_producto = request.form.get('Nombre_de_producto')
        Descripcion_de_producto = request.form.get('Descripcion_de_producto')
        codigo_producto = request.form.get('codigo_producto')
        categoria = request.form.get('categoria')
        stock = request.form.get('stock')
        precio = request.form.get('precio')

        nuevo_producto = Producto(
            ID_Producto = ID_Producto,
            Nombre_de_producto=Nombre_de_producto,
            Descripcion_de_producto=Descripcion_de_producto,
            codigo_producto=codigo_producto,
            categoria=categoria,
            stock=stock,
            precio=precio
        )

        session.add(nuevo_producto)
        session.commit()

        return redirect(url_for('Formulario_Producto'))  

    return render_template('Formulario_Producto.html') 

    
@app.route('/Lista_productos.html')
def Lista_productos():
    return render_template('Lista_productos.html')


@app.route('/Clientes.html', methods=['GET', 'POST'])
def Clientes():
    session = Session()

    if request.method == 'POST':
        nombre_cliente = request.form.get('Nombre_cliente')
        documento_tipo = request.form.get('documento_text')
        documento_numero = request.form.get('documento_numero')
        telefono = request.form.get('numero_celular')
        email = request.form.get('correo_cliente')
        fecha_nacimiento = request.form.get('fecha_nacimiento_clien')
        direccion = request.form.get('direccion_cliente')
        ciudad = request.form.get('ciudad_cliente')

        nuevo_cliente = Cliente(
            nombre=nombre_cliente,
            documento_tipo=documento_tipo,
            documento_numero=documento_numero,
            telefono=telefono,
            email=email,
            fecha_nacimiento=fecha_nacimiento,
            direccion=direccion,
            ciudad=ciudad
        )

        session.add(nuevo_cliente)
        session.commit()

        return redirect(url_for('Clientes'))
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



documento_tipo_enum = Enum(
    'Tarjeta de identidad',
    'Cédula de ciudadanía',
    'Cédula de extranjería',
    'Pasaporte',
    name='documento_tipo'
)

usuario_rol_enum = Enum(
    'Administrador',
    'Vendedor',
    'Bodega',
    name='usuario_rol'
)

producto_categoria_enum = Enum(
    'Computadoras y Accesorios',
    'Celulares y Accesorios',
    'Televisores y Audio',
    'Electrodomésticos pequeños',
    'Videojuegos y Consolas',
    'Redes y Conectividad',
    'Componentes y Repuestos',
    'Cámaras y Fotografía',
    'Baterías y Cargadores',
    'Otros accesorios',
    name='producto_categoria'
)

producto_stock_enum = Enum(
    'En camino',
    'Con Stock',
    'Sin Stock',
    name='producto_stock'
)

metodo_pago_enum = Enum(
    'Efectivo',
    'Tarjeta de crédito',
    'Tarjeta de débito',
    'Transferencia bancaria',
    name='metodo_pago'
)

class Cliente(ModeloBase):
    __tablename__ = 'Cliente'
    
    ID_Cliente = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    telefono = Column(Integer, nullable=False)
    direccion = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    documento_tipo = Column(documento_tipo_enum, nullable=False)
    documento_numero = Column(Integer, nullable=False, unique=True)
    fecha_nacimiento = Column(Date, nullable=False)
    ciudad = Column(String(100), nullable=False)
    
    facturas = relationship('Factura', backref='cliente', lazy=True)

class Usuario(ModeloBase):
    __tablename__ = 'Usuario'
    
    ID_Usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    telefono = Column(Integer, nullable=False)
    direccion = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    usuario = Column(String(12), nullable=False)
    contraseña = Column(String(255), nullable=False)
    rol = Column(usuario_rol_enum, nullable=False)
    fecha_alta = Column(Date, nullable=False)
    documento_tipo = Column(documento_tipo_enum, nullable=False)
    documento_numero = Column(Integer, nullable=False, unique=True)
    fecha_nacimiento = Column(Date, nullable=False)
    
    facturas = relationship('Factura', backref='usuario', lazy=True)



class Producto(ModeloBase):
    __tablename__ = 'Producto'
    
    ID_Producto = Column(Integer, primary_key=True, autoincrement=True)
    Nombre_de_producto = Column(String(255), nullable=False)
    Descripcion_de_producto = Column(Text, nullable=False)
    codigo_producto = Column(String(9), primary_key=True)
    categoria = Column(Enum('computadoras', 'celulares', 'tv', 'electrodomesticos', 'videojuegos', 'redes', 'componentes', 'camaras', 'baterias', 'otros'), nullable=False)
    stock = Column(Enum('encamino', 'constock', 'sinstock'), nullable=False)
    precio = Column(Numeric(10, 2), nullable=False)

    detalles = relationship('DetalleFactura', backref='producto', lazy=True)

def __init__(self, ID_Producto,Nombre_de_producto, Descripcion_de_producto, codigo_producto, categoria, stock, precio):
    self.ID_Producto = ID_Producto
    self.Nombre_de_producto = Nombre_de_producto
    self.Descripcion_de_producto = Descripcion_de_producto
    self.codigo_producto = codigo_producto
    self.categoria = categoria
    self.stock = stock
    self.precio = precio


class Factura(ModeloBase):
    __tablename__ = 'Factura'
    
    ID_factura = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    ID_Cliente = Column(Integer, ForeignKey('Cliente.ID_Cliente'), nullable=False)
    ID_Usuario = Column(Integer, ForeignKey('Usuario.ID_Usuario'), nullable=False)
    
    detalles = relationship('DetalleFactura', backref='factura', lazy=True)
    pagos = relationship('TipoPago', backref='factura', lazy=True)

class DetalleFactura(ModeloBase):
    __tablename__ = 'DetalleFactura'
    
    ID_Detalle = Column(Integer, primary_key=True, autoincrement=True)
    ID_Factura = Column(Integer, ForeignKey('Factura.ID_factura'), nullable=False)
    ID_Producto = Column(Integer, ForeignKey('Producto.ID_Producto'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)

class TipoPago(ModeloBase):
    __tablename__ = 'TipoPago'
    
    ID_Pago = Column(Integer, primary_key=True, autoincrement=True)
    monto = Column(Numeric(10, 2), nullable=False)
    metodoPago = Column(metodo_pago_enum, nullable=False)
    fecha = Column(Date, nullable=False)
    ID_Factura = Column(Integer, ForeignKey('Factura.ID_factura'), nullable=False)


ModeloBase.metadata.create_all(engine)