from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from .models import Usuario, Rol
from django.contrib.auth.hashers import check_password

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