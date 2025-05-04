from django.db import models
class Rol(models.Model):
    identificador = models.IntegerField(unique=True)  # antes: CharField
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class Usuario(models.Model):
    email = models.EmailField(primary_key=True, max_length=50)  # Primary Key
    nombre_completo = models.CharField(max_length=50)
    alias = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=180)
    fecha_nacimiento = models.DateField()
    direccion = models.TextField(null=True, blank=True, max_length=200)
    rol = models.ForeignKey(Rol, to_field='identificador', on_delete=models.CASCADE)  # FK a Rol.identificador

    def __str__(self):
        return f"{self.nombre_completo} ({self.alias})"


# tabla categoria: nombre_categoria. Terror, Acción, Mundo Abierto, Free To Play, Supervivencia.
class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)  # Primary Key
    nombre_categoria = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre_categoria

# Tabbla plataforma: id_plataforma, nombre_plataforma. Steam, Epic Games, Origin, Battle.net, PSN, Xbox.
class Plataforma(models.Model):
    id_plataforma = models.AutoField(primary_key=True)  # Primary Key
    nombre_plataforma = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre_plataforma

# Tabla juego: id_juego, categoria (fk a Categoria.id_categoria), nombre_juego, descripcion, cantidad_disponible, precio, imagen(url web biblioteca: //https://www.steamgriddb.com/ )
class Juego(models.Model):
    id_juego = models.AutoField(primary_key=True)  # Primary Key
    categoria = models.ForeignKey(Categoria, to_field='id_categoria', on_delete=models.CASCADE)  # FK a Categoria.id_categoria
    plataforma = models.ForeignKey(Plataforma, to_field='id_plataforma', on_delete=models.CASCADE)  # FK a Plataforma.id_plataforma
    nombre_juego = models.CharField(max_length=50, unique=True)  # Nombre como identificador único
    descripcion = models.TextField()
    cantidad_disponible = models.PositiveIntegerField()  # Ajustado para aceptar solo valores positivos
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Máximo 10 dígitos, 2 decimales
    imagen = models.URLField()

    def __str__(self):
        return self.nombre_juego
    
# Tabla Carrito: id_carrito, usuario (fk a Usuario.email), juego (fk a Juego.id_juego), cantidad, precio_total.
class Carrito(models.Model):
    id_carrito = models.AutoField(primary_key=True)  # Primary Key
    usuario = models.ForeignKey(Usuario, to_field='email', on_delete=models.CASCADE)  # FK a Usuario.email
    juego = models.ForeignKey(Juego, to_field='id_juego', on_delete=models.CASCADE)  # FK a Juego.id_juego
    cantidad = models.PositiveIntegerField()  # Ajustado para aceptar solo valores positivos
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)  # Máximo 10 dígitos, 2 decimales

    def __str__(self):
        return f"{self.usuario} - {self.juego}"
    
# Tabla compras: id_compra, usuario (fk a Usuario.email), juego (fk a Juego.id_juego), cantidad_compra, precio_total, fecha_compra, codigo_activación (PSN-12345-ABCDE / STEAM-67890-FGHIJ / XBOX-54321-KLMNO).
class Compra(models.Model):
    id_compra = models.AutoField(primary_key=True)  # Primary Key
    usuario = models.ForeignKey(Usuario, to_field='email', on_delete=models.CASCADE)  # FK a Usuario.email
    juego = models.ForeignKey(Juego, to_field='id_juego', on_delete=models.CASCADE)  # FK a Juego.id_juego
    codigo_activacion = models.CharField(max_length=50)  # Código de activación
    cantidad_compra = models.PositiveIntegerField()  # Ajustado para aceptar solo valores positivos
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)  # Máximo 10 dígitos, 2 decimales
    fecha_compra = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.juego} - {self.fecha_compra}"