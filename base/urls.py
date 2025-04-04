from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.LoginPage, name='login'),
    path('logout/', views.LogoutUser, name='logout'),
    path('register/', views.RegisterUser, name='register'),

    path('', views.HomePage, name='home'),
    path('quem-somos/', views.QuemSomosPage, name='quem_somos'),
    path('noticia/', views.NoticiaRedirect),
    path('noticia/<str:pk>/', views.NoticiaPage, name='noticia'),
    path('noticia/publicar/', views.NoticiaPage, name='publicar'),
    path('noticia/feed/', views.NoticiaPage, name='feed'),
    
    #{% url 'noticia' noticia.id %} 
]