# Generated by Django 5.1.7 on 2025-04-05 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_remove_noticia_arquivos_na_noticia_arquivonanoticia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arquivonanoticia',
            name='arquivo',
            field=models.FileField(blank=True, null=True, upload_to='Notícias .MD/arquivos/'),
        ),
    ]
