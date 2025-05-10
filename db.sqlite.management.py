import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'novashift.settings')
django.setup()

from core.models import Rol, Categoria, Plataforma, Usuario

def poblar_datos_iniciales():
    # Poblar tabla Rol
    Rol.objects.get_or_create(identificador=1, nombre='ADMINISTRADOR')
    Rol.objects.get_or_create(identificador=2, nombre='JUGADOR')
    Rol.objects.get_or_create(identificador=3, nombre='DESARROLLADOR')

    # Poblar tabla Categoria
    Categoria.objects.get_or_create(nombre_categoria='Terror')
    Categoria.objects.get_or_create(nombre_categoria='Acción')
    Categoria.objects.get_or_create(nombre_categoria='Mundo Abierto')
    Categoria.objects.get_or_create(nombre_categoria='Free To Play')
    Categoria.objects.get_or_create(nombre_categoria='Supervivencia')

    # Poblar tabla Plataforma
    Plataforma.objects.get_or_create(nombre_plataforma='Steam')
    Plataforma.objects.get_or_create(nombre_plataforma='Epic Games')
    Plataforma.objects.get_or_create(nombre_plataforma='Origin')
    Plataforma.objects.get_or_create(nombre_plataforma='Battle.net')
    Plataforma.objects.get_or_create(nombre_plataforma='PSN')
    Plataforma.objects.get_or_create(nombre_plataforma='Xbox')
    Plataforma.objects.get_or_create(nombre_plataforma='Nintendo')

    # Crear usuarios
    admin_role = Rol.objects.get(identificador=1)  # ADMINISTRADOR
    jugador_role = Rol.objects.get(identificador=2)  # JUGADOR
    desarrollador_role = Rol.objects.get(identificador=3)  # DESARROLLADOR

    Usuario.objects.get_or_create(
        email='michaelvzla@gmail.com',
        alias='michaelvzla',
        password='Mkg299....',  
        nombre_completo='Michael Vzla',
        fecha_nacimiento='1990-01-01',
        direccion='Dirección de Michael',
        rol=desarrollador_role
    )

    Usuario.objects.get_or_create(
        email='admin@novashift.cl',
        alias='admin',
        password='Mkg299....',  
        nombre_completo='Admin NovaShift',
        fecha_nacimiento='1985-01-01',
        direccion='Dirección del Admin',
        rol=admin_role
    )

    Usuario.objects.get_or_create(
        email='usuario2@gmail.com',
        alias='usuario2',
        password='Mkg299....',  
        nombre_completo='Usuario 2',
        fecha_nacimiento='1995-01-01',
        direccion='Dirección de Usuario 2',
        rol=jugador_role
    )

    print("Datos iniciales creados exitosamente.")

if __name__ == '__main__':
    poblar_datos_iniciales()

    # Verificar
    print(Rol.objects.all())
    print(Categoria.objects.all())
    print(Plataforma.objects.all())
    print(Usuario.objects.all())


