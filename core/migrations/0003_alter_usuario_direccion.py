# Generated by Django 5.2 on 2025-04-21 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_usuario_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='direccion',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]
