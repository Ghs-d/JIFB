from django.contrib import admin

# Register your models here.
from .models import Noticia, Comentario, ArquivoNaNoticia, Perfil, Resposta

admin.site.register(Perfil)
admin.site.register(Noticia)
admin.site.register(ArquivoNaNoticia)
admin.site.register(Comentario)
admin.site.register(Resposta)