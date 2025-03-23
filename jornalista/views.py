from django.shortcuts import render, redirect, get_object_or_404
from .forms import NoticiasForm
from django.http import HttpRequest
from .models import NotíciaModel
from django.contrib.auth.decorators import login_required

def publicar(request:HttpRequest):
    if request.method == "POST":
        formulario = NoticiasForm(request.POST)
        if formulario.is_valid:
            formulario.save()
            return redirect("news")

    contexto = {
        "form":NoticiasForm
    }
    return render(request, 'jornalista/publicar.html', contexto)


@login_required
def home_view(request):
    return render(request, 'jornalista/home.html')

def news_view(request):
    contexto = {
        "form":NoticiasForm,
        "notícias":NotíciaModel.objects.all()
    }
    return render(request, 'jornalista/news.html', contexto)

@login_required
def editar_news(request:HttpRequest, id):
    noticia = get_object_or_404(NotíciaModel, id=id)
    if request.method == "POST":
        formulario = NoticiasForm(request.POST, instance=noticia)
        if formulario.is_valid:
            formulario.save()
            return redirect("news")
    formulario = NoticiasForm(instance=noticia)
    contexto = {
        'form':formulario
    }
    return render(request, 'jornalista/editar.html', contexto)

@login_required
def remover_news(request:HttpRequest, id):
    noticia = get_object_or_404(NotíciaModel, id=id)
    noticia.delete()
    return redirect("news")

def quem_somos(request):
    return render(request, 'news/quemsomos.html')  # ghs


