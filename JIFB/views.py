from django.shortcuts import render
from jornalista.models import NotíciaModel
from jornalista.forms import NoticiasForm

def index_view(request):
    return render(request, 'news/home.html')

def news_view(request):
    contexto = {
        "form":NoticiasForm,
        "notícias":NotíciaModel.objects.all()
    }
    return render(request, 'news/news.html', contexto)
