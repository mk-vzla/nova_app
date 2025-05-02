import os

MI_API_KEY = os.environ.get('MI_API_KEY')


# sitio: https://www.giantbomb.com/api/search/?
if MI_API_KEY:
    # Variable configurada correctamente
    print(f"La API Key es: {MI_API_KEY}")
else:
    print("La variable de entorno MI_API_KEY no está definida.")
    # Maneja el caso en que la variable no esté configurada