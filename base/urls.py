from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.LoginPage, name='login'),
    path('logout/', views.LogoutUser, name='logout'),

    path('register/', views.RegisterUser, name='register'),

    path('noticia/', views.NoticiaRedirect),
    path('', views.HomePage, name='home'),
    path('procurar', views.Procurar, name='procurar'),
    path('quem-somos/', views.QuemSomosPage, name='quem_somos'),
    path('publicar/', views.NoticiaPublicar, name='publicar'),
    path('editar/<str:pk>/', views.NoticiaEditar, name='editar'),
    path('excluir/<str:pk>/', views.NoticiaExcluir, name='excluir'),
    path('noticia/<str:pk>/', views.NoticiaPage, name='noticia'),
    path('noticia/feed/', views.NoticiaPage, name='feed'),
]