from django.db import models

class Registro(models.Model):
    nombre_completo = models.CharField(max_length=50)  # NOT NULL
    alias = models.CharField(max_length=15, unique=True)  # NOT NULL
    email = models.EmailField(unique=True)  # NOT NULL
    password = models.CharField(max_length=18)  # NOT NULL
    fecha_nacimiento = models.DateField()  # NOT NULL
    direccion = models.TextField(null=True, blank=True)  # Opcional
    ROL_CHOICES = [
        (1, 'Administrador'),
        (2, 'Jugador'),
        (3, 'Desarrollador'),
    ]
    rol = models.IntegerField(choices=ROL_CHOICES, default=2)  # NOT NULL
    # terminos = models.BooleanField(default=False)  # NOT NULL

    def __str__(self):
        return f"{self.nombre_completo} ({self.alias})"