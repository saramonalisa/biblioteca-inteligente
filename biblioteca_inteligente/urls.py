from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('inicio/', views.inicio, name='inicio'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('cadastro_livro/', views.cadastro_livro, name='cadastro_livro'),
    path('editar_livro/<int:id_livro>/', views.editar_livro, name='editar_livro'),
    path('editar_emprestimo/<int:id>/', views.editar_emprestimo, name='editar_emprestimo'),
    path('detalhar_livro/<int:id_livro>/', views.detalhar_livro, name='detalhar_livro'),
    path('deletar_livro/<int:id_livro>/', views.deletar_livro, name='deletar_livro'),
    path('cadastro_emprestimo/', views.cadastro_emprestimo, name='cadastro_emprestimo'),
    path('ver_emprestimos/', views.ver_emprestimos, name='ver_emprestimos'),
    path('gerenciar_emprestimos/', views.gerenciar_emprestimos, name='gerenciar_emprestimos'),
    path('gerenciar_livros/', views.gerenciar_livros, name='gerenciar_livros'),
    path("ajax-messages/", views.ajax_mensagens, name="ajax_mensagens"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("ajax-livros/", views.ajax_livros, name="ajax_livros"),
    path("ajax-detalhar-livro/<int:id_livro>/", views.ajax_detalhar_livro, name="ajax_detalhar_livro"),
]