import os
import django

# Configurar el entorno de Django 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'novashift.settings')
django.setup()

import pymysql
pymysql.install_as_MySQLdb()

from core.models import Rol, Categoria, Plataforma, Usuario, Juego, Compra 

# def eliminar_todos_los_usuarios():
#     # Eliminar todos los usuarios
#     Usuario.objects.all().delete()
#     print("Todos los usuarios han sido eliminados.")

# if __name__ == '__main__':
#     # Llamar a la función para eliminar usuarios
#     eliminar_todos_los_usuarios()


# Poblar todas las tablas con los datos de la base de datos anterior de Oracle
def poblar_juegos():
    # Ruta al archivo de datos
    archivo = os.path.join(os.path.dirname(__file__), 'bd_anterior.txt')

    with open(archivo, 'r', encoding='utf-8') as file:
        for linea in file:
            # Dividir la línea en columnas
            datos = linea.strip().split('\t')
            if len(datos) != 7:
                print(f"Línea inválida: {linea}")
                continue

            # Extraer los datos
            nombre = datos[0]
            descripcion = datos[1]
            stock = int(datos[2])
            precio = float(datos[3])
            imagen = datos[4]
            categoria_id = int(datos[5])
            plataforma_id = int(datos[6])

            # Obtener las relaciones de categoría y plataforma
            try:
                categoria = Categoria.objects.get(id_categoria=categoria_id)
                plataforma = Plataforma.objects.get(id_plataforma=plataforma_id)
            except Categoria.DoesNotExist:
                print(f"Categoría con ID {categoria_id} no encontrada. Saltando...")
                continue
            except Plataforma.DoesNotExist:
                print(f"Plataforma con ID {plataforma_id} no encontrada. Saltando...")
                continue

            # Crear o actualizar el juego
            juego, creado = Juego.objects.get_or_create(
                nombre_juego=nombre,
                defaults={
                    'descripcion': descripcion,
                    'cantidad_disponible': stock,
                    'precio': precio,
                    'imagen': imagen,
                    'categoria': categoria,
                    'plataforma': plataforma,
                }
            )
            if creado:
                print(f"Juego creado: {nombre}")
            else:
                print(f"Juego ya existente: {nombre}")

if __name__ == '__main__':
    poblar_juegos()




# Código deshabilitado para evitar su ejecución
# import pymysql

# timeout = 10
# connection = pymysql.connect(
#   charset="utf8mb4",
#   connect_timeout=timeout,
#   cursorclass=pymysql.cursors.DictCursor,
#   db="defaultdb",
#   host="mysql-2fd182bc-novashift.g.aivencloud.com",
#   password="AVNS_JDCbhaVs2EXQkNGREyp",
#   read_timeout=timeout,
#   port=24542,
#   user="avnadmin",
#   write_timeout=timeout,
# )
  
# try:
#   cursor = connection.cursor()
#   cursor.execute("CREATE TABLE mytest (id INTEGER PRIMARY KEY)")
#   cursor.execute("INSERT INTO mytest (id) VALUES (1), (2)")
#   cursor.execute("SELECT * FROM mytest")
#   print(cursor.fetchall())
# finally:
#   connection.close()