from django.shortcuts import render
from jornalista.models import NotíciaModel
from jornalista.forms import NoticiasForm
from django.contrib.auth.decorators import login_required

def index_view(request):
    return render(request, 'news/index.html')

def news_view(request):
    usuario = request.user
    pertence_ao_jornalismo = usuario.groups.filter(name="Jornalista").exists()
    contexto = {
        "form":NoticiasForm,
        "notícias":NotíciaModel.objects.all(),
        'pertence_ao_jornalismo':pertence_ao_jornalismo
    }
    return render(request, 'news/news.html', contexto)

def login_view(request):
    return render(request, 'news/login.html')

@login_required
def dashboard_jornalista(request):
    usuario = request.user
    pertence_ao_jornalismo = usuario.groups.filter(name="Jornalista").exists()
    return render(request, 'news/index.html', {'pertence_ao_jornalismo':pertence_ao_jornalismo})

