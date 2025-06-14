from django.shortcuts import render, redirect
import json, requests, os, random, string
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from .models import Usuario, Rol, Categoria, Plataforma, Juego, Carrito, Compra
from django.contrib.auth.hashers import check_password
from .contra_aleatoria import generar_contraseña_aleatoria
from urllib.parse import quote
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models_copy import CopiaJuego, AliasSugerido
from .serializers import CopiaJuegoSerializer, AliasSugeridoSerializer
from django.utils.timezone import now


@csrf_exempt
def registrar(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Validar si el alias ya está registrado
            if Usuario.objects.filter(alias=data['alias']).exists():
                return JsonResponse({'error': 'El alias ya está registrado.'}, status=409)

            # Validación de rol
            try:
                rol_id = int(data['rol'])
                rol_obj = Rol.objects.get(identificador=rol_id)
            except (Rol.DoesNotExist, ValueError):
                return JsonResponse({'error': 'El rol especificado no existe.'}, status=400)

            # Crear usuario
            nuevo_usuario = Usuario.objects.create(
                email=data['email'],
                nombre_completo=data['nombre_completo'],
                alias=data['alias'],
                password=make_password(data['password']),
                fecha_nacimiento=data['fecha_nacimiento'],
                direccion=data.get('direccion', ''),
                rol=rol_obj
            )

            # Eliminar el alias de la tabla AliasSugerido si existe
            AliasSugerido.objects.filter(alias=data['alias']).delete()

            return JsonResponse({'mensaje': 'Usuario registrado correctamente.'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido.'}, status=405)

@csrf_exempt
def iniciar_sesion(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        alias = data.get('alias')
        password = data.get('password')

        if not alias or not password:
            return JsonResponse({'success': False, 'error': 'Alias y contraseña son obligatorios.'}, status=400)
        
        try:
            usuario = Usuario.objects.get(alias=alias)
            if check_password(password, usuario.password):
                # Guardar datos en la sesión
                request.session['conectado_alias'] = usuario.alias
                request.session['conectado_rol_id'] = int(usuario.rol.identificador)
                request.session['conectado_nombre_completo'] = usuario.nombre_completo
                request.session['conectado_direccion'] = usuario.direccion
                request.session['conectado_password'] = data.get('password')
                request.session['conectado_email'] = usuario.email  # Asegúrate de guardar el email aquí

                return JsonResponse({'success': True, 'mensaje': 'Inicio de sesión exitoso.'})
            else:
                return JsonResponse({'success': False, 'error': 'Contraseña incorrecta.'}, status=401)
        except Usuario.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'El alias no existe.'}, status=404)
    
    return JsonResponse({'success': False, 'error': 'Método no permitido.'}, status=405)



@csrf_exempt
def editar_usuario(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            email = data.get('email')
            usuario = Usuario.objects.get(email=email)

            usuario.nombre_completo = data.get('nombre_completo')
            usuario.alias = data.get('alias')
            usuario.fecha_nacimiento = data.get('fecha_nacimiento')
            usuario.direccion = data.get('direccion')

            rol_id = data.get('rol')
            rol = Rol.objects.get(identificador=rol_id)
            usuario.rol = rol

            usuario.save()

            return JsonResponse({'mensaje': 'Usuario actualizado correctamente.'})
        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado.'}, status=404)
        except Rol.DoesNotExist:
            return JsonResponse({'error': 'Rol no válido.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    

@csrf_exempt
def eliminar_usuario(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')

            # Buscar y eliminar al usuario
            usuario = Usuario.objects.get(email=email)
            usuario.delete()

            return JsonResponse({'mensaje': 'Usuario eliminado correctamente.'})
        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    

@csrf_exempt
def modificar_perfil(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Obtener el alias del usuario conectado desde la sesión
            alias = request.session.get('conectado_alias')
            if not alias:
                return JsonResponse({'error': 'Usuario no autenticado.'}, status=401)

            # Buscar el usuario por alias
            usuario = Usuario.objects.get(alias=alias)

            # Actualizar los campos del usuario
            usuario.nombre_completo = data.get('nombre', usuario.nombre_completo)
            usuario.direccion = data.get('direccion', usuario.direccion)

            # Validar y actualizar la contraseña
            password1 = data.get('password1')
            password2 = data.get('password2')
            if password1 and password1 == password2:
                usuario.password = make_password(password1)

            usuario.save()
            return JsonResponse({'mensaje': 'Perfil actualizado correctamente.'})
        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método no permitido.'}, status=405)


@csrf_exempt
def agregar_producto(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))

            # Validación de campos obligatorios
            campos_obligatorios = ['categoria', 'plataforma', 'nombre', 'descripcion', 'cantidad', 'precio']
            for campo in campos_obligatorios:
                if campo not in data:
                    return JsonResponse({'error': f'El campo {campo} es obligatorio.'}, status=400)
                # Validación de categoría
                try:
                    categoria_id = int(data['categoria'])  # esto lanza ValueError si no es convertible
                    categoria = Categoria.objects.get(id_categoria=categoria_id)
                except (Categoria.DoesNotExist, ValueError):
                    return JsonResponse({'error': 'La categoría especificada no existe.'}, status=400)

                # Validación de plataforma
                try:
                    plataforma_id = int(data['plataforma'])  # esto lanza ValueError si no es convertible
                    plataforma = Plataforma.objects.get(id_plataforma=plataforma_id)
                except (Plataforma.DoesNotExist, ValueError):
                    return JsonResponse({'error': 'La plataforma especificada no existe.'}, status=400)

            # Crear producto
            nuevo_producto = Juego.objects.create(
                categoria=categoria,
                plataforma=plataforma,
                nombre_juego=data['nombre'],
                descripcion=data['descripcion'],
                cantidad_disponible=data['cantidad'],
                precio=data['precio'],
                imagen=data['imagen']
            )
            return JsonResponse({'success': True, 'mensaje': 'Producto añadido exitosamente.'}, status=201)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Método no permitido.'}, status=405)


@csrf_exempt
def obtener_producto(request, producto_id):
    if request.method == 'GET':
        try:
            juego = Juego.objects.get(id_juego=producto_id)
            data = {
                'id': juego.id_juego,
                'categoria': juego.categoria.id_categoria,
                'plataforma': juego.plataforma.id_plataforma,
                'nombre': juego.nombre_juego,
                'descripcion': juego.descripcion,
                'imagen': juego.imagen,
                'cantidad': juego.cantidad_disponible,
                'precio': juego.precio,
            }
            return JsonResponse(data, status=200)
        except Juego.DoesNotExist:
            return JsonResponse({'error': 'Producto no encontrado.'}, status=404)
    return JsonResponse({'error': 'Método no permitido.'}, status=405)


@csrf_exempt
def modificar_producto(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            juego = Juego.objects.get(id_juego=data['producto_id'])

            juego.nombre_juego = data['nombre']
            juego.descripcion = data['descripcion']
            juego.imagen = data['imagen']
            juego.cantidad_disponible = data['cantidad']
            juego.precio = data['precio']

            # Validar y asignar categoría
            try:
                categoria_id = int(data['categoria'])
                categoria = Categoria.objects.get(id_categoria=categoria_id)
                juego.categoria = categoria
            except (Categoria.DoesNotExist, ValueError):
                return JsonResponse({'error': 'La categoría especificada no existe.'}, status=400)

            # Validar y asignar plataforma
            try:
                plataforma_id = int(data['plataforma'])
                plataforma = Plataforma.objects.get(id_plataforma=plataforma_id)
                juego.plataforma = plataforma
            except (Plataforma.DoesNotExist, ValueError):
                return JsonResponse({'error': 'La plataforma especificada no existe.'}, status=400)

            juego.save()

            return JsonResponse({'mensaje': 'Producto actualizado exitosamente.'})
        except Juego.DoesNotExist:
            return JsonResponse({'error': 'Producto no encontrado.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido.'}, status=405)


################################################################################################################################ ENVÍO DE MAILTRAP
@csrf_exempt
def enviar_correo_recuperacion(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')

            if not email:
                return JsonResponse({'error': 'El campo email es obligatorio.'}, status=400)

            if Usuario.objects.filter(email=email).exists():
                # Generar una nueva contraseña aleatoria
                usuario = Usuario.objects.get(email=email)

                # Enviar correo con Mailtrap PELIGRO, PELIGRO WARNING, NO SE DEBEN HARDCODEAR LAS CLAVES EN EL CÓDIGO
                api_token = "be5779fe18bc66bdbac3eb0cafe9a1b2"
                mailtrap_id = "3630156"
                from_email = "password@novashift.com"
                from_name = "Nova Shift"
                subject = "Recuperación de Contraseña"
                password = generar_contraseña_aleatoria()
                # Actualizar la contraseña del usuario en la base de datos
                usuario.password = make_password(password)
                usuario.save()
                # body_text = "Se ha solicitado un cambio de contraseña. Si no has solicitado este cambio, ignora este mensaje."
                body_html = f"""
                <html>
                    <p>Se ha solicitado un cambio de contraseña. Si no has solicitado este cambio, ignora este mensaje.</p>
                    <p>Tu contraseña es: <strong>{password}</strong></p>
                    <p>Puedes iniciar sesión en <a href="http://127.0.0.1:8000/login">Nova Shift</a>.</p>
                    <p>Saludos,<br>Equipo Nova Shift</p>
                </html>
                """
                url = f"https://sandbox.api.mailtrap.io/api/send/{mailtrap_id}"
                headers = {
                    "Authorization": f"Bearer {api_token}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "from": {"email": from_email, "name": from_name},
                    "to": [{"email": email}],
                    "subject": subject,
                    #"text": body_text,
                    "html": body_html,
                    "category": "Recuperación"
                }

                try:
                    response = requests.post(url, headers=headers, data=json.dumps(payload))
                    response.raise_for_status()
                    print("- - - - - - - - Correo enviado exitosamente a través de Mailtrap! - - - - - - - - ")
                    return JsonResponse({'mensaje': 'Correo de recuperación enviado exitosamente.'}, status=200)
                except requests.exceptions.RequestException as e:
                    return JsonResponse({'error': f'Error al enviar el correo: {str(e)}'}, status=500)

            else:
                return JsonResponse({'error': 'El correo no está registrado.'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido.'}, status=405)



################################################################################################################################ API DE GIANTBOMB (GET)
def buscar_juego(request):
    """
    Busca juegos en la API de GiantBomb y devuelve un JSON con
    los campos: name, aliases, deck, image.medium_url,
    original_release_date, platforms, original_game_rating.
    """
    # — Construir la URL con field_list para limitar los campos —
    query = request.GET.get('query', '').strip()
    query_encoded = quote(f'"{query}"')
    api_key = os.environ['MI_API_KEY']  # asume que siempre existe
    url = (
        "https://www.giantbomb.com/api/search/"
        f"?api_key={api_key}"
        "&format=json"
        f"&query={query_encoded}"
        "&resources=game"
        "&field_list=name,aliases,deck,image,original_release_date,platforms,original_game_rating"
    )

    # — Headers requeridos por GiantBomb —
    headers = {
        'User-Agent': 'NovaShiftApp/1.0',
        'Accept': 'application/json'
    }

    try:
        # — Llamada y parsing —
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # — Normalizar resultados —
        raw_results = data.get('results') or []
        resultados = []
        for juego in raw_results:
            resultados.append({
                'name': juego.get('name', 'N/A'),
                'aliases': juego.get('aliases', 'N/A'),
                'deck': juego.get('deck', 'N/A'),
                'image': juego.get('image', {}).get('medium_url', 'N/A'),
                'original_release_date': juego.get('original_release_date', 'N/A'),
                'platforms': [p.get('name', 'N/A') for p in juego.get('platforms') or []],
                'original_game_rating': [r.get('name', 'N/A') for r in juego.get('original_game_rating') or []],
            })

        # — Devolver JSON con resultados —
        return JsonResponse({'resultados': resultados}, status=200)

    except requests.exceptions.HTTPError as http_err:
        return JsonResponse(
            {'error': f'HTTP error al consumir la API: {http_err}'},
            status=response.status_code
        )
    except Exception as e:
        return JsonResponse(
            {'error': f'Error al consumir la API: {str(e)}'},
            status=500
        )



################################################################################################################################ API LOCAL 01
class CopiaJuegoListAPIView(APIView):
    def get(self, request):
        copias = CopiaJuego.objects.all().values('nombre_juego', 'descripcion', 'precio', 'imagen')
        serializer = CopiaJuegoSerializer(copias, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

def lista_copias_json(request):
    copias = CopiaJuego.objects.all().values('nombre_juego', 'descripcion', 'precio', 'imagen')
    return JsonResponse(list(copias), safe=False)


################################################################################################################################ API LOCAL 02
class AliasSugeridoCreateAPIView(APIView):
    def post(self, request):
        serializer = AliasSugeridoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def obtener_alias_sugeridos(request):
    # Obtén todos los alias de la tabla AliasSugerido
    alias_sugeridos = AliasSugerido.objects.values_list('alias', flat=True)
    
    # Excluir los alias que ya existen en la tabla Usuario
    alias_registrados = Usuario.objects.values_list('alias', flat=True)
    alias_disponibles = set(alias_sugeridos) - set(alias_registrados)
    
    # Selecciona 5 alias aleatorios de los disponibles
    alias_aleatorios = random.sample(list(alias_disponibles), min(len(alias_disponibles), 5))
    
    return JsonResponse({'alias_sugeridos': alias_aleatorios})



################################################################################################################################ AGREGAR AL CARRITO
@csrf_exempt
def agregar_al_carrito(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            producto_id = data.get('producto_id')
            conectado_email = request.session.get('conectado_email')  # Obtener el email desde la sesión
            conectado_rol_id = request.session.get('conectado_rol_id')  # Obtener el rol del usuario conectado

            if not conectado_email:
                return JsonResponse({'error': 'Usuario no conectado.'}, status=401)

            # Validar si el usuario tiene rol 1 o 3
            if conectado_rol_id in [1, 3]:
                return JsonResponse({'error': 'No se puede comprar con cuenta administrador/desarrollador.'}, status=403)

            usuario = Usuario.objects.get(email=conectado_email)
            juego = Juego.objects.get(id_juego=producto_id)

            # Verificar si el usuario ya tiene el juego en el carrito
            if Carrito.objects.filter(usuario=usuario, juego=juego).exists():
                return JsonResponse({'error': 'Ya tienes este juego en tu carrito. Solo puedes añadir una unidad.'}, status=400)

            # Agregar el juego al carrito
            Carrito.objects.create(
                usuario=usuario,
                juego=juego,
                cantidad=1,
                precio_total=juego.precio
            )

            return JsonResponse({'mensaje': 'Juego añadido al carrito exitosamente.'}, status=200)

        except Juego.DoesNotExist:
            return JsonResponse({'error': 'El juego no existe.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido.'}, status=405)



################################################################################################################################ VISTA DEL CARRITO
def checkout(request):
    conectado_email = request.session.get('conectado_email')  # Obtener el email del usuario conectado

    if not conectado_email:
        return redirect('login')  # Redirigir al login si no hay usuario conectado

    # Normalizar el email por seguridad
    conectado_email = conectado_email.strip().lower()

    # Obtener productos del carrito
    productos_carrito = Carrito.objects.filter(usuario__email=conectado_email)

    total_precio = sum(item.precio_total for item in productos_carrito)
   
    return render(request, 'checkout.html', {
        'productos_carrito': productos_carrito,
        'total_precio': total_precio,
    })

################################################################################################################################ ELIMINAR DEL CARRITO
@csrf_exempt
def eliminar_del_carrito(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            producto_id = data.get('producto_id')
            conectado_email = request.session.get('conectado_email')  # Obtener el email desde la sesión

            if not conectado_email:
                return JsonResponse({'error': 'Usuario no conectado.'}, status=401)

            usuario = Usuario.objects.get(email=conectado_email)
            juego = Juego.objects.get(id_juego=producto_id)

            # Eliminar el producto del carrito
            Carrito.objects.filter(usuario=usuario, juego=juego).delete()

            return JsonResponse({'mensaje': 'Producto eliminado del carrito exitosamente.'}, status=200)
        except Juego.DoesNotExist:
            return JsonResponse({'error': 'Producto no encontrado.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método no permitido.'}, status=405)



################################################################################################################################ PROCESAR PAGO
@csrf_exempt
def proceder_al_pago(request):
    if request.method == 'POST':
        try:
            conectado_email = request.session.get('conectado_email')  # Obtener el email del usuario conectado
            if not conectado_email:
                return JsonResponse({'error': 'Usuario no conectado.'}, status=401)

            usuario = Usuario.objects.get(email=conectado_email)
            carrito_items = Carrito.objects.filter(usuario=usuario)

            if not carrito_items.exists():
                return JsonResponse({'error': 'El carrito está vacío.'}, status=400)

            # Procesar cada producto en el carrito
            for item in carrito_items:
                juego = item.juego

                # Verificar si hay suficiente cantidad disponible
                if juego.cantidad_disponible == 0:
                    return JsonResponse({'error': f'Producto SIN STOCK Pago Revertido: {juego.nombre_juego}.'}, status=400)
                if juego.cantidad_disponible < item.cantidad:
                    return JsonResponse({'error': f'No hay suficiente stock para el juego {juego.nombre_juego}.'}, status=400)

                # Restar la cantidad comprada del stock
                juego.cantidad_disponible -= item.cantidad
                juego.save()

                # Generar un código de activación único
                codigo_activacion = f"{juego.plataforma.nombre_plataforma[:3].upper()}-{random.randint(10000, 99999)}-{''.join(random.choices(string.ascii_uppercase, k=5))}"

                # Crear un registro en el historial de compras
                Compra.objects.create(
                    usuario=usuario,
                    juego=juego,
                    codigo_activacion=codigo_activacion,
                    cantidad_compra=item.cantidad,
                    precio_total=item.precio_total,
                    fecha_compra=now()
                )

            # Eliminar los productos del carrito
            carrito_items.delete()

            return JsonResponse({'mensaje': 'Compra realizada exitosamente.'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método no permitido.'}, status=405)



################################################################################################################################ VISTA DE MIS COMPRAS
def mis_compras_realizadas(request):
    conectado_email = request.session.get('conectado_email')  # Obtener el email del usuario conectado
    if not conectado_email:
        return redirect('login')  # Redirigir al login si no hay usuario conectado

    # Obtener todas las compras del usuario conectado
    compras = Compra.objects.filter(usuario__email=conectado_email).select_related('juego', 'juego__plataforma')

    return render(request, 'mis_compras.html', {'compras': compras})



################################################################################################################################ BUSCAR JUEGOS
def buscar_juegos(request):
    query = request.GET.get('q', '').strip()
    juegos = []

    if len(query) >= 3:  # Validar que el mínimo de caracteres sea 3
        juegos = Juego.objects.filter(nombre_juego__icontains=query)

    return render(request, 'resultados.html', {'juegos': juegos, 'query': query})