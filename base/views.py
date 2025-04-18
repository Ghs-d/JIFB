from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.core import exceptions
from django.db.models import Q
from pathlib import Path

from .forms import NoticiaForm, ArquivosForm, ArquivoFormSet, EditarUserProfileForm
from .models import Noticia, ArquivoNaNoticia, Comentario, Perfil


def QuemSomosPage(request):
    return render(request, 'base/quemsomos.html', {'foto_de_perfil':Perfil.objects.get(user=request.user).foto_de_perfil if request.user.is_authenticated else None})


def RedirectToHome(request):
    return redirect('home')


def NotFoundPage(request):
    return render(request, '404.html')


def LoginPage(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
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
            user.username = user.username.lower()
            user.save()
            Perfil.objects.create(
                user=user,
                pode_comentar=True,
                pode_alterar_foto_de_perfil=True,
                foto_de_perfil="foto_de_perfis/default.jpg"
            )

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

    noticias = Noticia.objects.all().order_by('-updated')
    if request.user.is_authenticated:
        perfil = Perfil.objects.filter(user=request.user)
        context = {
        'noticias':noticias,
        'perfil':perfil,
        'foto_de_perfil':Perfil.objects.get(user=request.user).foto_de_perfil
    }
    else:
        context = {
            'noticias':noticias,
            'perfil':None,
            'foto_de_perfil':None
        }
    return render(request, "base/index.html", context)


def Procurar(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    número_de_notícia = 0
    noticias = Noticia.objects.all().order_by('-updated').filter(
        Q(título__icontains=q) &
        Q(visivel=True)
        )
    número_de_notícia = noticias.count()
    if request.user.is_authenticated:  
        foto_de_perfil = Perfil.objects.get(user=request.user).foto_de_perfil
    else:
        foto_de_perfil = None
    context = {
        'noticias':noticias,    
        'número_de_notícia':número_de_notícia,
        'foto_de_perfil':foto_de_perfil
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
        'noticia_form':noticia_form,
        'foto_de_perfil':Perfil.objects.get(user=request.user).foto_de_perfil
    }
    return render(request, "base/noticia_form.html", context)



def NoticiaPage(request, pk):
    if pk.isnumeric():
        noticia = get_object_or_404(Noticia, pk=pk)

        arquivos = list(ArquivoNaNoticia.objects.filter(noticia=noticia).values('arquivos'))
 
        comentarios = list(Comentario.objects.filter(noticia=noticia))

        if noticia.visivel == True:
            conteudo_html = noticia.corpo

            if request.method == 'POST':
                if not request.user.is_authenticated:
                    return redirect('login')
                
                elif request.user.perfil.pode_comentar == False:
                    return HttpResponse('<h1>Você está proibido de comentar</h1>')

                else:
                    comentario = Comentario.objects.create(
                        autor=Perfil.objects.get(user=request.user),
                        noticia=noticia,
                        body=request.POST.get('body')
                    )

                    return JsonResponse({
                        'id': comentario.id,
                        'body': comentario.body,
                        'autor': comentario.autor.user.username,
                        'foto': comentario.autor.foto_de_perfil.url if hasattr(comentario.autor.foto_de_perfil, 'url') else f"/static/media/{comentario.autor.foto_de_perfil}",
                        'data': comentario.created.strftime('%d %b %Y - %H:%M')
                    })

            if request.user.is_authenticated:  
                foto_de_perfil = Perfil.objects.get(user=request.user).foto_de_perfil
            else:
                foto_de_perfil = None
            context = {
                'conteudo_html':conteudo_html,
                'noticia':noticia,
                'arquivos':arquivos,
                'comentarios':comentarios,
                'foto_de_perfil':foto_de_perfil
            }
            return render(request, "base/template_news.html", context)
        
        elif noticia.visivel == False and request.user.is_staff == True:
            conteudo_html = noticia.corpo

            context = {
                'conteudo_html':conteudo_html,
                'noticia':noticia,
                'arquivos':arquivos,
                'comentarios':comentarios,
                'aviso':"Essa notícia não está visível para os usuários",
                'foto_de_perfil':Perfil.objects.get(user=request.user).foto_de_perfil
            }
            return render(request, "base/template_news.html", context)
        

        elif noticia.visivel == False and request.user.is_staff == False:
            return redirect('feed')
        
        else:
            return redirect('feed')
        
    elif pk == 'feed':
        noticias = Noticia.objects.all().order_by('-updated')
        if request.user.is_authenticated:  
            foto_de_perfil = Perfil.objects.get(user=request.user).foto_de_perfil
        else:
            foto_de_perfil = None
        context = {
            'noticias':noticias,
            'foto_de_perfil':foto_de_perfil
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

    foto_de_perfil = Perfil.objects.get(user=request.user).foto_de_perfil


    context = {
        'noticia_form': noticia_form,
        'arquivos_formset': arquivos_formset,
        'noticia': noticia,
        'foto_de_perfil':foto_de_perfil
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

    return render(request, "base/excluir.html", {
                                                'obj': noticia,
                                                'foto_de_perfil':Perfil.objects.get(user=request.user).foto_de_perfil
                                                })


@login_required(login_url='/login')
def UserProfile(request, pk):
    usuario = User.objects.get(username=pk)

    perfil = Perfil.objects.get(user=usuario)
    foto_perfil = perfil.foto_de_perfil
    print(foto_perfil)

    context = {
        "usuario":usuario,
        "foto_perfil":foto_perfil,
        "perfil":perfil
    }
    return render(request, "base/profile_user.html", context)


@login_required(login_url='/login')
def EditarUserProfile(request, pk):
    usuario = User.objects.get(username=pk)

    perfil = Perfil.objects.get(user=usuario)
    
    if request.method == 'POST':
        Path(perfil.foto_de_perfil.path).unlink(missing_ok=True)
        profile_form = EditarUserProfileForm(request.POST, request.FILES)
        
        if profile_form.is_valid():

            perfil.bio = profile_form.cleaned_data['bio']
            perfil.foto_de_perfil = profile_form.cleaned_data['foto_de_perfil']
            
            perfil.save()
            return redirect('user', pk)

    else:
        profile_form = EditarUserProfileForm(instance=perfil)

    context = {
        "profile_form":profile_form,
    }
    return render(request, "base/editar_profile.html", context)


@login_required(login_url='/login')
def ComentarioExcluir(request, pk):
    comentario = Comentario.objects.get(id=pk)

    

    if request.method == 'POST':
        # Exclui arquivos relacionados à notícia
        if request.user.is_staff == False or request.user.username != comentario.autor.user.username:
            return HttpResponse("<h1>Somente o autor ou um moderador pode excluir!</h1>")
        
        elif request.user.is_staff == True or request.user.username == comentario.autor.user.username:
            comentario.delete()
        
        return redirect('noticia', comentario.noticia.id)

    return render(request, "base/excluir.html", {
                                                'obj': comentario,
                                                'foto_de_perfil':Perfil.objects.get(user=request.user).foto_de_perfil
                                                })