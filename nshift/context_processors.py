def session_data(request):
    """
    Agrega los datos de la sesión al contexto de todas las plantillas.
    """
    return {
        'conectado_alias': request.session.get('conectado_alias', None),
        'conectado_rol_id': request.session.get('conectado_rol_id', None),
    }