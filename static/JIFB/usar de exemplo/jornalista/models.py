from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class NotíciaModel(models.Model):
    tituto = models.CharField(max_length=150)
    noticia = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True) 
    mostrar_noticia = models.BooleanField(default=False)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.títuto_noticia
    
class Message(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    noticia = models.ForeignKey(NotíciaModel, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50] 