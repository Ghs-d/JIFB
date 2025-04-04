from django.db import models
from django.contrib.auth.models import User
from django import forms
# Create your models here.

class Noticia(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    título = models.CharField(max_length=200)
    
    noticia = models.FileField(upload_to="Notícias .MD/%Y/%m/%d/", blank=True, null=True)
    arquivos_na_noticia = models.ImageField(upload_to="static/Notícias .MD/imagem", blank=True, null=True)
    capa_noticia = models.ImageField(upload_to="Notícias .MD/CAPAS/%Y/%m/%d/", blank=True, null=True)

    visivel = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.título
    
class Mensagem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.body[0:50]
    