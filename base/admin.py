from django.contrib import admin

# Register your models here.
from .models import Noticia, Mensagem, ArquivoNaNoticia, Perfil

admin.site.register(Perfil)
admin.site.register(Noticia)
admin.site.register(Mensagem)
admin.site.register(ArquivoNaNoticia)