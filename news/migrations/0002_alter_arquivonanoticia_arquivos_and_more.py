# Generated by Django 5.1.7 on 2025-04-20 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arquivonanoticia',
            name='arquivos',
            field=models.FileField(blank=True, null=True, upload_to='uploads/noticias/arquivos/'),
        ),
        migrations.AlterField(
            model_name='noticia',
            name='capa_noticia',
            field=models.ImageField(upload_to='uploads/noticias .MD/CAPAS/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='noticia',
            name='corpo',
            field=models.FileField(upload_to='uploads/noticias/%Y/%m/%d/'),
        ),
    ]
