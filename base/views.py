from django.shortcuts import render, get_object_or_404, redirect
from .models import Noticia
import markdown2
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
    return render(request, 'base/index.html', context)


def QuemSomosPage(request):
    return render(request, 'base/quemsomos.html')

def NoticiaRedirect(request):
    return redirect('feed/')

def NoticiaPage(request, pk):
    if pk == 'feed':
        noticias = Noticia.objects.all()

        context = {
            'noticias':noticias,
        }

        return render(request, "base/news.html", context)
    
    elif pk != 'feed':
        noticias = Noticia.objects.all()
        noticia = get_object_or_404(Noticia, pk=pk)

        # Ler o conteúdo do arquivo Markdown
        with noticia.noticia.open("rb") as f:
            conteudo_markdown = f.read().decode("utf-8")
        
        # Converter Markdown para HTML
        conteudo_html = markdown2.markdown(conteudo_markdown)

        context = {
            'conteudo_html':conteudo_html,
            'noticia':noticia
        }
        return render(request, "base/template_news.html", context)