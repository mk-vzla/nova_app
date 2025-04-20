
import random
import string

def generar_contraseña_aleatoria():
    caracteres = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.sample(caracteres, 10))

