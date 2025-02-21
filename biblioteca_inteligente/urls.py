from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('inicio/', views.inicio, name='inicio'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('cadastro_livro/', views.cadastro_livro, name='cadastro_livro'),
    path('cadastro_emprestimo/', views.cadastro_emprestimo, name='cadastro_emprestimo'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('ver_emprestimos/', views.ver_emprestimos, name='ver_emprestimos'),
    path('configuracoes/', views.configuracoes, name='configuracoes'),
]