from django.shortcuts import render, redirect
from core.models import Usuario, Juego, Carrito
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import requests, random


# Create your views here.
# index, accion, administrador, checkout, free_to_play, inventario, login, mis_compras, mundo_abierto, perfil, quienes_somos, recuperar_contra, registro, supervivencia, terror, usuarios

def inicio(request):
    conectado_alias = request.session.get('conectado_alias', None)  
    conectado_rol_id = request.session.get('conectado_rol_id', None)  
    conectado_nombre_completo = request.session.get('conectado_nombre_completo', None)  
    conectado_direccion = request.session.get('conectado_direccion', None)  
    conectado_password = request.session.get('conectado_password', None)  
    return render(request, 'index.html', {'conectado_alias': conectado_alias, 'conectado_rol_id': conectado_rol_id, 
                                          'conectado_nombre_completo': conectado_nombre_completo, 'conectado_direccion': conectado_direccion,
                                            'conectado_password': conectado_password})

def accion (request):
    return render(request, 'accion.html')

def administrador(request):
    return render(request, 'administrador.html')

def checkout(request):
    conectado_email = request.session.get('conectado_email', None)
    productos_carrito = Carrito.objects.select_related('juego__plataforma').filter(usuario__email=conectado_email)
    total_precio = sum(producto.juego.precio for producto in productos_carrito)
    return render(request, 'checkout.html', {
        'productos_carrito': productos_carrito,
        'total_precio': total_precio,
    })

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

def mini_juego(request):
    return render(request, 'mini_juego.html')

def mostrar_api_nova(request):
    return render(request, 'api_nova.html')


# Elimina todos los datos de la sesión
def desconectarse(request):
    request.session.flush()  
    return redirect('inicio')  

# Una función para listar todos los usuarios
def listar_usuarios(request):
    usuarios = Usuario.objects.select_related('rol')  # Carga el rol asociado
    return render(request, 'usuarios.html', {'usuarios': usuarios})

@csrf_exempt
def mostrar_inventario(request):
    # Obtener el parámetro de ordenación
    orden = request.GET.get('orden', 'id_juego')
    direccion = request.GET.get('dir', 'desc')  # 'asc' o 'desc'

    # Mapear alias de columnas para ordenamiento
    valid_fields = {
        'id_juego': 'id_juego',
        'categoria': 'categoria__nombre_categoria',
        'nombre_juego': 'nombre_juego',
        'precio': 'precio',
        'cantidad_disponible': 'cantidad_disponible',
    }
    sort_field = valid_fields.get(orden, 'id_juego')
    prefix = '' if direccion == 'asc' else '-'

    # Obtener los juegos ya ordenados
    juegos = (Juego.objects
              .select_related('categoria', 'plataforma')  # Include platform
              .order_by(f'{prefix}{sort_field}'))

    return render(request, 'inventario.html', {
        'juegos': juegos,
        'current_order': orden,
        'current_dir': direccion,
    })



@csrf_exempt
def eliminar_juego(request, id_juego):
    if request.method == 'POST':
        juego = get_object_or_404(Juego, id_juego=id_juego)
        juego.delete()
    return redirect('mostrar_inventario')



################################################################################################# FRONT FRONT Juegos
# funcion para mostrar juegos categorías; terror, acción, mundo abierto, free to play, supervivencia.
def mostrar_terror(request):
    # Filtrar juegos por la categoría "Terror" y con cantidad disponible mayor a 0
    juegos = Juego.objects.filter(categoria__nombre_categoria='Terror', cantidad_disponible__gt=0).select_related('plataforma')
    return render(request, 'terror.html', {'juegos': juegos})

def mostrar_accion(request):
    # Filtrar juegos por la categoría "Acción" y con cantidad disponible mayor a 0
    juegos = Juego.objects.filter(categoria__nombre_categoria='Acción', cantidad_disponible__gt=0).select_related('plataforma')
    return render(request, 'accion.html', {'juegos': juegos})

def mostrar_mundo_abierto(request):
    # Filtrar juegos por la categoría "Mundo Abierto" y con cantidad disponible mayor a 0
    juegos = Juego.objects.filter(categoria__nombre_categoria='Mundo Abierto', cantidad_disponible__gt=0).select_related('plataforma')
    return render(request, 'mundo_abierto.html', {'juegos': juegos})

def mostrar_free_to_play(request):
    # Filtrar juegos por la categoría "Free To Play" y con cantidad disponible mayor a 0
    juegos = Juego.objects.filter(categoria__nombre_categoria='Free To Play', cantidad_disponible__gt=0).select_related('plataforma')
    return render(request, 'free_to_play.html', {'juegos': juegos})

def mostrar_supervivencia(request):
    # Filtrar juegos por la categoría "Supervivencia" y con cantidad disponible mayor a 0
    juegos = Juego.objects.filter(categoria__nombre_categoria='Supervivencia', cantidad_disponible__gt=0).select_related('plataforma')
    return render(request, 'supervivencia.html', {'juegos': juegos})


# Mostrar 1 juego de cada categoría en la página de inicio
def mostrar_juegos_inicio(request):
    juegos_terror = list(Juego.objects.filter(categoria__nombre_categoria='Terror', cantidad_disponible__gt=0)[:1])
    juegos_accion = list(Juego.objects.filter(categoria__nombre_categoria='Acción', cantidad_disponible__gt=0)[:1])
    juegos_mundo_abierto = list(Juego.objects.filter(categoria__nombre_categoria='Mundo Abierto', cantidad_disponible__gt=0)[:1])
    juegos_supervivencia = list(Juego.objects.filter(categoria__nombre_categoria='Supervivencia', cantidad_disponible__gt=0)[:1])

    # Unir todas las listas
    juegos_todos = juegos_terror + juegos_accion + juegos_mundo_abierto + juegos_supervivencia

    # Agrupar de a 2
    juegos_pares = [juegos_todos[i:i+2] for i in range(0, len(juegos_todos), 2)]

    return render(request, 'index.html', {
        'juegos_pares': juegos_pares,
    })


################################################################################################# Mini Juego API
URL = "https://pokeapi.co/api/v2/pokemon"

# haré un formulario para que el usuario responda el tipo de pokemon que se menciona en la api. esto estará en un formulario en el template mini_juego.html
# el metodo es get, mostrando el pokemon, ejemplo Pikachu.
# El formulario tiene predefinidas todas las especioes (tipo) y el usuario elige una de esas. No necesito hacer ningún post hacia pokepi.
# importé random, para que seleccione de forma aleatoria un pokemon de la api, y lo muestre en el template mini_juego.html

# Sabiendo que https://pokeapi.co/api/v2/pokemon/ditto me trae el pokemon ditto, por ejemplo.
# y si haces un for de este pokemon, te trae el tipo o los tipos de de ese pokemon consultado. ejemplo:
# for type in data['types']:
#     print(type['type']['name'])
# considerar que seleccionar un tipo de varios, sería una respuesta correcta.

@csrf_exempt
def mini_juego(request):
    tipos_disponibles = {
    'water': 'Agua',
    'steel': 'Acero',
    'bug': 'Bicho',
    'dragon': 'Dragón',
    'electric': 'Eléctrico',
    'ghost': 'Fantasma',
    'fire': 'Fuego',
    'fairy': 'Hada',
    'ice': 'Hielo',
    'fighting': 'Lucha',
    'normal': 'Normal',
    'grass': 'Planta',
    'psychic': 'Psíquico',
    'rock': 'Roca',
    'dark': 'Siniestro',
    'ground': 'Tierra',
    'poison': 'Veneno',
    'flying': 'Volador',
}

    # “nuevo Pokémon” si viene new=1
    nuevo = request.GET.get('new') == '1'

    # Inicializa o recupera sesión
    intentos = request.session.setdefault('intentos', 0)
    aciertos = request.session.setdefault('aciertos', 0)

    # Determina el Pokémon actual
    if nuevo or 'current_pokemon' not in request.session:
        resp = requests.get('https://pokeapi.co/api/v2/pokemon?limit=1025')
        if resp.status_code == 200:
            elegido = random.choice(resp.json()['results'])
            current = elegido['name']
        else:
            current = 'pikachu'
        request.session['current_pokemon'] = current
    else:
        current = request.session['current_pokemon']

    tipo_seleccionado = request.GET.get('tipo')
    nombre_pokemon = current

    imagen_url = None
    tipos_pokemon_ing = []
    tipos_pokemon_es = []

    # Si ya seleccionó y hay menos de 10 intentos, procesa la respuesta
    if tipo_seleccionado and intentos < 10:
        resp = requests.get(f'https://pokeapi.co/api/v2/pokemon/{nombre_pokemon}')
        if resp.status_code == 200:
            data = resp.json()
            imagen_url = data['sprites']['front_default']
            tipos_pokemon_ing = [t['type']['name'] for t in data['types']]
        tipos_pokemon_es = [tipos_disponibles[t] for t in tipos_pokemon_ing if t in tipos_disponibles]

        intentos += 1
        if tipo_seleccionado in tipos_pokemon_ing:
            aciertos += 1

        request.session['intentos'] = intentos
        request.session['aciertos'] = aciertos

    else:
        # Primera vez, o después de 10 intentos, o recarga sin enviar
        resp = requests.get(f'https://pokeapi.co/api/v2/pokemon/{nombre_pokemon}')
        if resp.status_code == 200:
            imagen_url = resp.json()['sprites']['front_default']
        # tipos_pokemon_ing y es quedan vacíos hasta que se evalúe

    promedio = round((aciertos / intentos) * 100) if intentos > 0 else 0
    tipo_seleccionado_es = tipos_disponibles.get(tipo_seleccionado, '')

    return render(request, 'mini_juego.html', {
        'nombre_pokemon': nombre_pokemon,
        'imagen_url': imagen_url,
        'tipos_disponibles': tipos_disponibles,
        'tipo_seleccionado': tipo_seleccionado,
        'tipo_seleccionado_es': tipo_seleccionado_es,
        'tipos_pokemon_ing': tipos_pokemon_ing,
        'tipos_pokemon_es': tipos_pokemon_es,
        'intentos': intentos,
        'aciertos': aciertos,
        'promedio': promedio
    })


def reiniciar_juego(request):
    request.session['intentos'] = 0
    request.session['aciertos'] = 0
    # Eliminar Pokémon actual para forzar uno nuevo
    request.session.pop('current_pokemon', None)
    return redirect('mini_juego')
