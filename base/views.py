from django.shortcuts import render, get_object_or_404
from .models import Noticia
import markdown
import os
# Create your views here.
def LoginPage(request):
    return render(request, 'base/login.html')

def RegisterUser(request):
    pass

def LogoutUser(request):
    pass

def HomePage(request):
    noticas = Noticia.objects.all()
    context = {
        'noticias':noticas
    }
    return render(request, 'base/home.html', context)


def QuemSomosPage(request):
    return render(request, 'base/quemsomos.html')



def NoticiaPage(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)

    # Ler o conteúdo do arquivo Markdown
    with noticia.noticia.open("rb") as f:
        conteudo_markdown = f.read().decode("utf-8")
    
    # Converter Markdown para HTML
    conteudo_html = markdown.markdown(conteudo_markdown)

    return render(request, "base/template_news.html", {"conteudo_html": conteudo_html})