# Generated by Django 5.2 on 2025-04-14 04:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_usuario_rol'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='rol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.rol', to_field='identificador'),
        ),
    ]
