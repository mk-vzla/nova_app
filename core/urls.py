# filepath: c:\Users\micha\Documentos\DUOCUC\5toBimestre\ProgramacionWEB\semana4\django\novashift\nova_app\core\urls.py
from django.urls import path
from . import views



urlpatterns = [
    path('registrar/', views.registrar, name='registrar'),
    path('conectarse/', views.iniciar_sesion, name='iniciar_sesion'),
    path('editar/', views.editar_usuario, name='editar_usuario'),
    path('eliminar/', views.eliminar_usuario, name='eliminar_usuario'),
]