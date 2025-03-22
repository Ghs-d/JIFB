from django.db import models

# Create your models here.
class NotíciaModel(models.Model):
    tituto = models.CharField(max_length=150)
    noticia = models.TextField(max_length=1000)
    data_de_criacao = models.DateTimeField(auto_now_add=True)
    mostrar_noticia = models.BooleanField(default=False)
    autor = models.CharField(max_length=20)

    def __str__(self):
        return self.títuto_noticia