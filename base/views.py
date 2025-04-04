from django.shortcuts import render, get_object_or_404, redirect
from .models import Noticia, ArquivoNaNoticia
from .forms import NoticiaForm, ArquivosForm



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
    noticias = Noticia.objects.all()
    context = {
        'noticias':noticias
    }
    return render(request, "base/index.html", context)


def QuemSomosPage(request):
    return render(request, 'base/quemsomos.html')

def NoticiaRedirect(request):
    return redirect('feed')

def NoticiaPage(request, pk):
    if pk == 'feed':
        noticias = Noticia.objects.all()

        context = {
            'noticias':noticias,
        }

        return render(request, "base/news.html", context)
    
    elif pk == 'publicar':
        if request.method == 'POST':
            noticia_form = NoticiaForm(request.POST, request.FILES)
            arquivo_form = ArquivosForm(request.POST, request.FILES)
            arquivos = request.FILES.getlist('arquivos_na_noticia')
            
            if noticia_form.is_valid() and arquivo_form.is_valid():
                noticia = noticia_form.save(commit=False)
                noticia.autor = request.user
                noticia.save()
                
                for arquivo in request.FILES.getlist('arquivos'):
                    ArquivoNaNoticia.objects.create(noticia=noticia, arquivo=arquivo)
                
                return redirect('feed')
        else:
            noticia_form = NoticiaForm()
            arquivo_form = ArquivosForm()
        
        
        context = {
            'arquivo_form':arquivo_form,
            'noticia_form':noticia_form
        }
        return render(request, "base/noticia_form.html", context)


    elif pk.isnumeric():
        noticias = Noticia.objects.all()
        noticia = get_object_or_404(Noticia, pk=pk)

        # Ler o conteúdo do arquivo Markdown
        with noticia.corpo.open("rb") as f:
            conteudo_markdown = f.read().decode("utf-8")
        
        # Converter Markdown para HTML
        conteudo_html = markdown2.markdown(conteudo_markdown)

        context = {
            'conteudo_html':conteudo_html,
            'noticia':noticia
        }
        return render(request, "base/template_news.html", context)
    
    else:
        return redirect('feed')
