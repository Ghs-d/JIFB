from django.urls import path
from . import views

urlpatterns = [
    path("publicar/", views.publicar),
    path("", views.home_view),
    path("news/", views.news_view, name = 'news'),
    path("editar/<int:id>", views.editar_news, name = 'editar'),
    path("remover/<int:id>", views.remover_news, name = 'remover')
]
