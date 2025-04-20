from django.urls import path, include
from .views import inicio, accion, administrador, checkout, free_to_play, inventario, supervivencia, terror, desconectarse
from .views import listar_usuarios, login, mis_compras, mundo_abierto, perfil, quienes_somos, recuperar_contra, registro, mostrar_inventario, eliminar_juego

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
    path('usuarios', listar_usuarios, name='listar_usuarios'),
    path('desconectarse', desconectarse, name='desconectarse'),
    path('inventario/', mostrar_inventario, name='mostrar_inventario'),
    path('eliminar_juego/<int:id_juego>/', eliminar_juego, name='eliminar_juego'),
]

