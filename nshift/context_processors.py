from core.models import Usuario, Carrito

def session_data(request):
    """
    Agrega los datos de la sesión al contexto de todas las plantillas.
    Consulta la base de datos para obtener información actualizada del usuario conectado.
    """
    conectado_alias = request.session.get('conectado_alias', None)
    conectado_rol_id = request.session.get('conectado_rol_id', None)
    conectado_nombre_completo = None
    conectado_direccion = None
    conectado_email = None  # Nuevo campo para el email

    if conectado_alias:
        try:
            # Consultar la base de datos para obtener los datos más recientes
            usuario = Usuario.objects.get(alias=conectado_alias)
            conectado_nombre_completo = usuario.nombre_completo
            conectado_direccion = usuario.direccion
            conectado_email = usuario.email  # Obtener el email del usuario
            productos_carrito = Carrito.objects.filter(usuario__email=conectado_email)
        except Usuario.DoesNotExist:
            # Si el usuario no existe, limpiar la sesión
            request.session.flush()

    return {
        'conectado_alias': conectado_alias,
        'conectado_rol_id': conectado_rol_id,
        'conectado_nombre_completo': conectado_nombre_completo,
        'conectado_direccion': conectado_direccion,
        'conectado_email': conectado_email,  # Agregar el email al contexto
        'conectado_password': request.session.get('conectado_password', None),
        'productos_carrito': productos_carrito if 'productos_carrito' in locals() else None,
    }