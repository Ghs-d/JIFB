# Generated by Django 5.1.7 on 2025-04-15 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0024_alter_comentario_autor_alter_perfil_foto_de_perfil'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='bio',
            field=models.TextField(default='Eu sou novo aqui!'),
        ),
    ]
