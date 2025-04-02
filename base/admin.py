from django.contrib import admin

# Register your models here.
from .models import Noticia, Mensagem

admin.site.register(Noticia)
admin.site.register(Mensagem)