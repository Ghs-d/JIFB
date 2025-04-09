from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory
from django.core.exceptions import MultipleObjectsReturned
import os
from pathlib import Path

from .models import Noticia, ArquivoNaNoticia
from .forms import NoticiaForm, ArquivosForm

BASE_DIR = Path(__file__).resolve().parent.parent

def LoginPage(request):
    return render(request, 'base/login.html')

def RegisterUser(request):
    return render(request, 'base/register.html')

def LogoutUser(request):
    pass

def QuemSomosPage(request):
    return render(request, 'base/quemsomos.html')

def NoticiaRedirect(request):
    return redirect('feed')


def HomePage(request):
    noticias = Noticia.objects.all().order_by('updated')
    context = {
        'noticias':noticias
    }
    return render(request, "base/index.html", context)


def NoticiaPublicar(request):
    if request.method == 'POST':
        noticia_form = NoticiaForm(request.POST, request.FILES)
        arquivo_form = ArquivosForm(request.POST, request.FILES)
            
        if noticia_form.is_valid() and arquivo_form.is_valid():
            noticia = noticia_form.save(commit=False)
            noticia.autor = request.user
            noticia.save()
            
            for arquivo in request.FILES.getlist('arquivos'):
                ArquivoNaNoticia.objects.create(noticia=noticia, arquivos=arquivo)
            
            return redirect('feed')
    else:
        noticia_form = NoticiaForm()
        arquivo_form = ArquivosForm()
        
        
    context = {
        'arquivo_form':arquivo_form,
        'noticia_form':noticia_form
    }
    return render(request, "base/noticia_form.html", context)


def NoticiaEditar(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)

    if request.method == 'POST':

        noticia_form = NoticiaForm(request.POST, request.FILES, instance=noticia)

        arquivos = request.FILES.getlist('arquivos')
        print(arquivos)
        if noticia_form.is_valid():
            os.remove(os.path.join(BASE_DIR/ 'static', 'media', noticia.capa_noticia))
            os.remove(os.path.join(BASE_DIR/ 'static', 'media', noticia.corpo))

            noticia = noticia_form.save(commit=False)
            noticia.autor = request.user
            noticia.save()
            
            for arq in arquivos:
                ArquivoNaNoticia.objects.create(noticia=noticia, arquivos=arq)

            return redirect('home')

    else:
        noticia_form = NoticiaForm(instance=noticia)

    context = {
        'noticia_form': noticia_form,
    }
    return render(request, "base/editar.html", context)



def NoticiaPage(request, pk):
    if pk.isnumeric():
        noticia = get_object_or_404(Noticia, pk=pk)

        arquivos = list(ArquivoNaNoticia.objects.filter(noticia=noticia).values('arquivos'))
 

        if pk.isnumeric():
            conteudo_html = noticia.corpo

            context = {
                'conteudo_html':conteudo_html,
                'noticia':noticia,
                'arquivos':arquivos,
            }
            return render(request, "base/template_news.html", context)
        else:
            return redirect('feed')
        
    elif pk == 'feed':
        noticias = Noticia.objects.all().order_by('updated')

        context = {
            'noticias':noticias,
        }

        return render(request, "base/news.html", context)

    else:
        return redirect('feed')


def NoticiaExcluir(request, pk):
    noticia = Noticia.objects.get(id=pk)
    print(noticia)
    if request.method == 'POST':
        os.remove(os.path.join(BASE_DIR/ 'static', 'media', noticia.capa_noticia))
        os.remove(os.path.join(BASE_DIR/ 'static', 'media', noticia.corpo))
        arquivos = list(ArquivoNaNoticia.objects.filter(noticia=noticia).values('arquivos'))
        for arquivo in arquivos:
            os.remove(os.path.join(BASE_DIR/ 'static', 'media', arquivo.arquivos))

        
        noticia.delete()
        return redirect('feed')

    return render(request, "base/excluir.html", {'obj':noticia})