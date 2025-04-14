from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.core import exceptions
from django.contrib import messages
from django.http import HttpResponse
import os
from pathlib import Path
import pathlib

from .models import Noticia, ArquivoNaNoticia
from .forms import NoticiaForm, ArquivosForm, ArquivoFormSet

BASE_DIR = Path(__file__).resolve().parent.parent


def QuemSomosPage(request):
    return render(request, 'base/quemsomos.html')


def NoticiaRedirect(request):
    return redirect('feed')


def LoginPage(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Usuário não existe!')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Nome de usuário OU senha estão erradas!')

    context = {

    }
    return render(request, 'base/login.html', context)

def RegisterUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid:
            user = form.save(commit=False)
            user.username = user.username
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Ocorreu um erro durante o registro!')
    return render(request, 'base/register.html', {'form':form})

@login_required(login_url='/login')
def LogoutUser(request):
    logout(request)
    return redirect('home')



def HomePage(request):

    noticias = Noticia.objects.all().order_by('updated')
    context = {
        'noticias':noticias
    }
    return render(request, "base/index.html", context)


def Procurar(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    número_de_notícia = 0
    noticias = Noticia.objects.all().order_by('updated').filter(
        Q(título__icontains=q)
        )
    número_de_notícia = noticias.count()

    context = {
        'noticias':noticias,
        'número_de_notícia':número_de_notícia
    }
    return render(request, "base/procurar.html", context)



@login_required(login_url='/login')
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


def NoticiaPage(request, pk):
    if pk.isnumeric():
        noticia = get_object_or_404(Noticia, pk=pk)

        arquivos = list(ArquivoNaNoticia.objects.filter(noticia=noticia).values('arquivos'))
 
        print(noticia)
        if noticia.visivel == False:
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
        return redirect('home')
    
    
@login_required(login_url='/login')
def NoticiaEditar(request, pk):

    noticia = Noticia.objects.get(id=pk)

    if not request.user.is_staff:
        return HttpResponse("<h1>Somente o autor pode alterar alguma coisa dessa notícia!</h1>")


    if request.method == 'POST':

        noticia_form = NoticiaForm(request.POST, request.FILES, instance=noticia)
        arquivos_formset = ArquivoFormSet(request.POST, request.FILES, queryset=ArquivoNaNoticia.objects.filter(noticia=noticia))
        arquivos = ArquivoNaNoticia.objects.filter(noticia=noticia)


        if noticia_form.is_valid() and arquivos_formset.is_valid():
            noticia = noticia_form.save(commit=False)
            noticia.autor = request.user
            arquivos = arquivos_formset.save(commit=False)
            noticia_form.save()
            
            # Esse loop vai salvar os arquivos editados
            for arquivo in arquivos:
                arquivo.noticia = noticia
                arquivo.save()
            print(f"Arquivos marcados pra deletar: {[a.id for a in arquivos_formset.deleted_objects]}")
            
            # Esse loop vai deletar os arquivos
            for obj in arquivos_formset.deleted_objects:
                arquivos = ArquivoNaNoticia.objects.filter(noticia=obj.noticia)

                for arquivo in arquivos:
                    try:
                        Path(arquivo.arquivos.path).unlink(missing_ok=True)  # apaga do disco
                        arquivo.delete()  # apaga do banco
                    except Exception as e:
                        print(f"Erro ao excluir {arquivo.arquivos.name}: {e}")

                obj.delete()  

                
            novos_arquivos = request.FILES.getlist('novos_arquivos')
            
            # Esse loop vai criar novos Arquivos
            for arq in novos_arquivos:
                ArquivoNaNoticia.objects.create(noticia=noticia, arquivos=arq)
            
            return redirect('home')

    else:
        noticia_form = NoticiaForm(instance=noticia)
        arquivos_formset = ArquivoFormSet(queryset=ArquivoNaNoticia.objects.filter(noticia=noticia))



    context = {
        'noticia_form': noticia_form,
        'arquivos_formset': arquivos_formset,
        'noticia': noticia
    }
    return render(request, "base/editar.html", context)




@login_required(login_url='/login')
def NoticiaExcluir(request, pk):
    noticia = Noticia.objects.get(id=pk)

    if not request.user.is_staff:
        return HttpResponse("<h1>Somente o autor pode alterar alguma coisa dessa notícia!</h1>")

    if request.method == 'POST':
        # Exclui arquivos relacionados à notícia
        arquivos = ArquivoNaNoticia.objects.filter(noticia=noticia.id)
        for arquivo in arquivos:
            try:
                Path(arquivo.arquivos.path).unlink(missing_ok=True)
            except Exception as e:
                print(f"Erro ao excluir : {e}")
        arquivos.delete()
        
        
        # Exclui possíveis arquivos diretos da notícia
        if noticia.capa_noticia:
            Path(noticia.capa_noticia.path).unlink(missing_ok=True)
        if noticia.corpo:
            Path(noticia.corpo.path).unlink(missing_ok=True)

        noticia.delete()
        return redirect('feed')

    return render(request, "base/excluir.html", {'obj': noticia})