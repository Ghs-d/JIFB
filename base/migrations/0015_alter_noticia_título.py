# Generated by Django 5.2 on 2025-04-09 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_rename_arquivo_arquivonanoticia_arquivos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticia',
            name='título',
            field=models.CharField(max_length=500),
        ),
    ]
