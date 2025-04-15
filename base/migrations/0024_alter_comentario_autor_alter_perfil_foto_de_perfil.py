# Generated by Django 5.1.7 on 2025-04-15 22:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0023_rename_user_comentario_autor_perfil_foto_de_perfil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='autor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.perfil'),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='foto_de_perfil',
            field=models.ImageField(default='foto_de_perfis/default.jpg', upload_to='foto_de_perfis/'),
        ),
    ]
