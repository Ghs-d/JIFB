from django.db import models
from django.contrib.auth.models import User
from django import forms


class Noticia(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    título = models.CharField(max_length=500)
    
    corpo = models.FileField(upload_to="Notícias .MD/%Y/%m/%d/")
    capa_noticia = models.ImageField(upload_to="Notícias .MD/CAPAS/%Y/%m/%d/")

    visivel = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.título


class ArquivoNaNoticia(models.Model):
    noticia = models.ForeignKey(Noticia, related_name='arquivos', on_delete=models.CASCADE)
    arquivos = models.FileField(upload_to="Notícias .MD/arquivos/", blank=True, null=True)

    def __str__(self):
        return f"Arquivo de {self.noticia.título}"



class Mensagem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.body[0:50]
    