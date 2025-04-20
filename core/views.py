from django.shortcuts import render
import json, requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from .models import Usuario, Rol, Categoria, Plataforma, Juego
from django.contrib.auth.hashers import check_password
from .contra_aleatoria import generar_contraseña_aleatoria


@csrf_exempt
def registrar(request):
    if request.method == 'POST':
        print("solicitud recibida")
        data = json.loads(request.body.decode('utf-8'))
        print("datos recibidos:", data)

        # Validación campos obligatorios
        campos_obligatorios = ['email', 'nombre_completo', 'alias', 'password', 'fecha_nacimiento', 'rol']
        for campo in campos_obligatorios:
            if campo not in data:
                return JsonResponse({'error': f'El campo {campo} es obligatorio.'}, status=400)

        # Validación correo ya registrado
        if Usuario.objects.filter(email=data['email']).exists():
            return JsonResponse({'error': 'El correo ya está registrado.'}, status=409)
        
        # Validación alias ya registrado
        if Usuario.objects.filter(alias=data['alias']).exists():
            return JsonResponse({'error': 'El alias ya está registrado.'}, status=409)

        # Validación de rol // Solventando poroblema con la cuestión...
        try:
            rol_id = int(data['rol'])  # esto lanza ValueError si no es convertible
            rol_obj = Rol.objects.get(identificador=rol_id)
        except (Rol.DoesNotExist, ValueError):
            return JsonResponse({'error': 'El rol especificado no existe.'}, status=400)

        # Crear usuario
        try:
            nuevo_usuario = Usuario.objects.create(
                email=data['email'],
                nombre_completo=data['nombre_completo'],
                alias=data['alias'],
                password=make_password(data['password']),
                fecha_nacimiento=data['fecha_nacimiento'],
                direccion=data.get('direccion', ''),
                rol=rol_obj  # Asignar la instancia de Rol
            )
            return JsonResponse({'success': True, 'mensaje': 'Usuario registrado exitosamente.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Método no permitido.'}, status=405)

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
            # Verificar la contraseña usando check_password
            if check_password(password, usuario.password):
                # Guardar Alias de la sesión y su rol_id, forzando conectado_rol_id a int
                request.session['conectado_alias'] = usuario.alias
                request.session['conectado_rol_id'] = int(usuario.rol.identificador)
                request.session['conectado_nombre_completo'] = usuario.nombre_completo
                request.session['conectado_direccion'] = usuario.direccion
                request.session['conectado_password'] = data.get('password')

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
    return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def agregar_producto(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            print("Datos recibidos:", data)

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


############################################################################################ ENVÍO DE MAILTRAP

@csrf_exempt
def enviar_correo_recuperacion(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')

            if not email:
                return JsonResponse({'error': 'El campo email es obligatorio.'}, status=400)

            if Usuario.objects.filter(email=email).exists():
                import random, string
                # Generar una nueva contraseña aleatoria
                usuario = Usuario.objects.get(email=email)

                # Enviar correo con Mailtrap
                api_token = "6bf88bf3c945c740b7bf0d2cea4433c6"
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
                <body>
                    <p>Se ha solicitado un cambio de contraseña. Si no has solicitado este cambio, ignora este mensaje.</p>
                    <p>Tu contraseña es: <strong>{password}</strong></p>
                    <p>Puedes iniciar sesión en <a href="http://127.0.0.1:8000/login">Nova Shift</a>.</p>
                    <p>Saludos,<br>Equipo Nova Shift</p>
                </body>
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
                    print("Correo enviado exitosamente a través de Mailtrap!")
                    return JsonResponse({'mensaje': 'Correo de recuperación enviado exitosamente.'}, status=200)
                except requests.exceptions.RequestException as e:
                    return JsonResponse({'error': f'Error al enviar el correo: {str(e)}'}, status=500)

            else:
                return JsonResponse({'error': 'El correo no está registrado.'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido.'}, status=405)
