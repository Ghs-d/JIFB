from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE
        )
    
    bio = models.TextField(default="Eu sou novo aqui!")
    
    foto_de_perfil = models.ImageField(
        default="foto_de_perfis/default.jpg", 
        upload_to="foto_de_perfis/"
        )
    
    pode_comentar = models.BooleanField(
        default=True
        )
    
    pode_alterar_foto_de_perfil = models.BooleanField(
        default=True
        )

    def __str__(self):
        return self.user.username

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



class Comentario(models.Model):
    autor = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE)
    body = models.TextField()
    like = models.IntegerField(blank=True, null=True, default=0)
    dislike = models.IntegerField(blank=True, null=True, default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.body[0:50]
    