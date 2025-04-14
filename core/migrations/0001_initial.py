# Generated by Django 5.2 on 2025-04-14 04:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identificador', models.IntegerField(unique=True)),
                ('nombre', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('nombre_completo', models.CharField(max_length=50)),
                ('alias', models.CharField(max_length=15, unique=True)),
                ('password', models.CharField(max_length=18)),
                ('fecha_nacimiento', models.DateField()),
                ('direccion', models.TextField(blank=True, null=True)),
                ('rol', models.ForeignKey(default='default_id', on_delete=django.db.models.deletion.CASCADE, to='core.rol', to_field='identificador')),
            ],
        ),
    ]
