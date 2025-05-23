# Generated by Django 5.1.7 on 2025-04-04 23:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_alter_noticia_autor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='noticia',
            name='arquivos_na_noticia',
        ),
        migrations.CreateModel(
            name='ArquivoNaNoticia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arquivo', models.FileField(upload_to='static/Notícias .MD/arquivos/')),
                ('noticia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arquivos', to='base.noticia')),
            ],
        ),
    ]
