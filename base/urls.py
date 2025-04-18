from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.HomePage, name='home'),

    path('404', views.NotFoundPage, name='404'),

    path('login/', views.LoginPage, name='login'),
    path('logout/', views.LogoutUser, name='logout'),
    path('register/', views.RegisterUser, name='register'),

    path('procurar/', views.Procurar, name='procurar'),

    path('quem-somos/', views.QuemSomosPage, name='quem_somos'),

    path('noticia/', views.RedirectToHome),
    path('publicar/', views.NoticiaPublicar, name='publicar'),
    path('editar/<str:pk>/', views.NoticiaEditar, name='editar'),
    path('excluir/<str:pk>/', views.NoticiaExcluir, name='excluir'),
    path('noticia/<str:pk>/', views.NoticiaPage, name='noticia'),
    path('noticia/feed/', views.NoticiaPage, name='feed'),

    path('u/', views.RedirectToHome),
    path('u/<str:pk>', views.UserProfile, name='user'),
    path('u/editar/<str:pk>', views.EditarUserProfile, name='editar_user'),


    path('excluir-comentario/<str:pk>/', views.ComentarioExcluir, name='excluir-comentario'),


]