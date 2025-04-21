from django.shortcuts import render, redirect
from core.models import Usuario, Juego
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404


# Create your views here.
# index, accion, administrador, checkout, free_to_play, inventario, login, mis_compras, mundo_abierto, perfil, quienes_somos, recuperar_contra, registro, supervivencia, terror, usuarios

def inicio(request):
    conectado_alias = request.session.get('conectado_alias', None)  
    conectado_rol_id = request.session.get('conectado_rol_id', None)  
    conectado_nombre_completo = request.session.get('conectado_nombre_completo', None)  
    conectado_direccion = request.session.get('conectado_direccion', None)  
    conectado_password = request.session.get('conectado_password', None)  
    return render(request, 'index.html', {'conectado_alias': conectado_alias, 'conectado_rol_id': conectado_rol_id, 'conectado_nombre_completo': conectado_nombre_completo, 'conectado_direccion': conectado_direccion, 'conectado_password': conectado_password})

def accion (request):
    return render(request, 'accion.html')

def administrador(request):
    return render(request, 'administrador.html')

def checkout(request):
    return render(request, 'checkout.html')

def free_to_play(request):
    return render(request, 'free_to_play.html')

def inventario(request):
    return render(request, 'inventario.html')

def login(request):
    return render(request, 'login.html')

def mis_compras(request):
    return render(request, 'mis_compras.html')

def mundo_abierto(request):
    return render(request, 'mundo_abierto.html')

def perfil(request):
    return render(request, 'perfil.html')

def quienes_somos(request):
    return render(request, 'quienes_somos.html')

def recuperar_contra(request):
    return render(request, 'recuperar_contra.html')

def registro(request):
    return render(request, 'registro.html')

def supervivencia(request):
    return render(request, 'supervivencia.html')

def terror(request):
    return render(request, 'terror.html')

def usuarios(request):
    return render(request, 'usuarios.html')

def desconectarse(request):
    request.session.flush()  # Elimina todos los datos de la sesión
    return redirect('inicio')  

# Una función para listar todos los usuarios
def listar_usuarios(request):
    usuarios = Usuario.objects.select_related('rol')  # Carga el rol asociado
    return render(request, 'usuarios.html', {'usuarios': usuarios})

@csrf_exempt
def mostrar_inventario(request):
    juegos = Juego.objects.select_related('categoria').all()
    return render(request, 'inventario.html', {'juegos': juegos})

@csrf_exempt
def eliminar_juego(request, id_juego):
    if request.method == 'POST':
        juego = get_object_or_404(Juego, id_juego=id_juego)
        juego.delete()
    return redirect('mostrar_inventario')



################################################################################################# FRONT FRONT Ventas
# funcion para mostrar juegos categorías; terror, acción, mundo abierto, free to play, supervivencia.
def mostrar_terror(request):
    # Filtrar juegos por la categoría "Terror"
    juegos = Juego.objects.filter(categoria__nombre_categoria='Terror')  # Ajustado al modelo actual
    return render(request, 'terror.html', {'juegos': juegos})

def mostrar_accion(request):
    # Filtrar juegos por la categoría "Acción"
    juegos = Juego.objects.filter(categoria__nombre_categoria='Acción')  # Ajustado al modelo actual
    return render(request, 'accion.html', {'juegos': juegos})

def mostrar_mundo_abierto(request):
    # Filtrar juegos por la categoría "Mundo Abierto"
    juegos = Juego.objects.filter(categoria__nombre_categoria='Mundo Abierto')  # Ajustado al modelo actual
    return render(request, 'mundo_abierto.html', {'juegos': juegos})

def mostrar_free_to_play(request):
    # Filtrar juegos por la categoría "Free To Play"
    juegos = Juego.objects.filter(categoria__nombre_categoria='Free To Play')  # Ajustado al modelo actual
    return render(request, 'free_to_play.html', {'juegos': juegos})

def mostrar_supervivencia(request):
    # Filtrar juegos por la categoría "Supervivencia"
    juegos = Juego.objects.filter(categoria__nombre_categoria='Supervivencia')  # Ajustado al modelo actual
    return render(request, 'supervivencia.html', {'juegos': juegos})

# Mostrar 1 juego de cada categoría en la página de inicio
def mostrar_juegos_inicio(request):
    # Filtrar juegos por la categoría "Terror"
    juegos_terror = Juego.objects.filter(categoria__nombre_categoria='Terror')[:1]  # Ajustado al modelo actual
    # Filtrar juegos por la categoría "Acción"
    juegos_accion = Juego.objects.filter(categoria__nombre_categoria='Acción')[:1]  # Ajustado al modelo actual
    # Filtrar juegos por la categoría "Mundo Abierto"
    juegos_mundo_abierto = Juego.objects.filter(categoria__nombre_categoria='Mundo Abierto')[:1]  # Ajustado al modelo actual
    # Filtrar juegos por la categoría "Supervivencia"
    juegos_supervivencia = Juego.objects.filter(categoria__nombre_categoria='Supervivencia')[:1]  # Ajustado al modelo actual

    return render(request, 'index.html', {
        'juegos_terror': juegos_terror,
        'juegos_accion': juegos_accion,
        'juegos_mundo_abierto': juegos_mundo_abierto,
        'juegos_supervivencia': juegos_supervivencia,
    })