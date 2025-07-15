from .base import engine, Session, ModeloBase


# para poder mandar mis enums a cada modelito
from sqlalchemy import Enum

documento_tipo_enum = Enum(
    'Tarjeta de identidad', 'Cédula de ciudadanía', 'Cédula de extranjería', 'Pasaporte',
    name='documento_tipo'
)

usuario_rol_enum = Enum(
    'Administrador', 'Vendedor', 'Bodega',
    name='usuario_rol'
)

metodo_pago_enum = Enum(
    'Efectivo', 'Tarjeta de crédito', 'Tarjeta de débito', 'Transferencia bancaria',
    name='metodo_pago'
)


