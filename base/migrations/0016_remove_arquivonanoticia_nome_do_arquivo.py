# Generated by Django 5.1.7 on 2025-04-09 20:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_alter_noticia_título'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='arquivonanoticia',
            name='Nome_do_Arquivo',
        ),
    ]
