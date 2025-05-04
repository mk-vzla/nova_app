# filepath: c:\Users\micha\Documentos\DUOCUC\5toBimestre\ProgramacionWEB\semana4\django\novashift\nova_app\core\urls.py
from django.urls import path
from . import views
from .views import agregar_producto, buscar_juego, CopiaJuegoListAPIView, lista_copias_json



urlpatterns = [
    path('registrar/', views.registrar, name='registrar'),
    path('conectarse/', views.iniciar_sesion, name='iniciar_sesion'),
    path('editar/', views.editar_usuario, name='editar_usuario'),
    path('eliminar/', views.eliminar_usuario, name='eliminar_usuario'),
    path('modificar_perfil/', views.modificar_perfil, name='modificar_perfil'),
    path('agregar_producto/', agregar_producto, name='agregar_producto'),
    path('obtener_producto/<int:producto_id>/', views.obtener_producto, name='obtener_producto'),
    path('modificar_producto/', views.modificar_producto, name='modificar_producto'),
    path('recuperar_contra/', views.enviar_correo_recuperacion, name='enviar_correo_recuperacion'),
    path('buscar_juego/', views.buscar_juego, name='buscar_juego'),
    path('api/copias/', CopiaJuegoListAPIView.as_view(), name='lista-copias'),
    path('api/copias-json/', lista_copias_json, name='lista-copias-json')
]
