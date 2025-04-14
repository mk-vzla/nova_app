from django.db import models
class Rol(models.Model):
    identificador = models.IntegerField(unique=True)  # antes: CharField
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class Usuario(models.Model):
    email = models.EmailField(primary_key=True)  # Primary Key
    nombre_completo = models.CharField(max_length=50)
    alias = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=180)
    fecha_nacimiento = models.DateField()
    direccion = models.TextField(null=True, blank=True)
    rol = models.ForeignKey(Rol, to_field='identificador', on_delete=models.CASCADE)  # FK a Rol.identificador

    def __str__(self):
        return f"{self.nombre_completo} ({self.alias})"
