import random
import string

def generar_clave_pago(longitud=11):
    caracteres = string.ascii_uppercase + string.digits  # A-Z y 0-9
    return ''.join(random.choice(caracteres) for _ in range(longitud))