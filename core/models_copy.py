from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Juego


################################################################################################################################ Copia de tabla: Juego
class CopiaJuego(models.Model):
    id = models.AutoField(primary_key=True) 
    nombre_juego = models.CharField(max_length=50, unique=True)  #Nombre identificador unico, no se repite en la tabla Juego Original
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.URLField()

    def __str__(self):
        return self.nombre_juego

# Señal para sincronizar CopiaJuego con Juego
@receiver(post_save, sender=Juego)
def sincronizar_juego(sender, instance, **kwargs):
    CopiaJuego.objects.update_or_create(
        nombre_juego=instance.nombre_juego, 
        defaults={
            'descripcion': instance.descripcion,
            'precio': instance.precio,
            'imagen': instance.imagen,
        }
    )

# Señal para eliminar CopiaJuego al eliminar Juego
@receiver(post_delete, sender=Juego)
def eliminar_copia_juego(sender, instance, **kwargs):
    CopiaJuego.objects.filter(nombre_juego=instance.nombre_juego).delete()



################################################################################################################################ 