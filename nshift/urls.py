from django.urls import path, include
from .views import inicio, accion, administrador, checkout, free_to_play, inventario, listar_usuarios, login, mis_compras, mundo_abierto, perfil, quienes_somos, recuperar_contra, registro, supervivencia, terror, desconectarse

urlpatterns = [
    path('', inicio, name='inicio'),
    path('accion', accion, name='accion'),
    path('administrador', administrador, name='administrador'),
    path('checkout', checkout, name='checkout'),
    path('free_to_play', free_to_play, name='free_to_play'),
    path('inventario', inventario, name='inventario'),
    path('login', login, name='login'),
    path('mis_compras', mis_compras, name='mis_compras'),
    path('mundo_abierto', mundo_abierto, name='mundo_abierto'),
    path('perfil', perfil, name='perfil'),
    path('quienes_somos', quienes_somos, name='quienes_somos'),
    path('recuperar_contra', recuperar_contra, name='recuperar_contra'),
    path('registro', registro, name='registro'),
    path('supervivencia', supervivencia, name='supervivencia'),
    path('terror', terror, name='terror'),
    # path('usuarios', usuarios, name='usuarios'),
    path('desconectarse', desconectarse, name='desconectarse'),
    path('usuarios/', listar_usuarios, name='listar_usuarios'),    
]

