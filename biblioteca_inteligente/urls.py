# urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Páginas públicas
    path('', views.index, name='index'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Início
    path('inicio/', views.inicio, name='inicio'),
    
    # Livros
    path('livros/', views.inicio, name='livros'),
    path('livro/<int:id_livro>/', views.detalhar_livro, name='detalhar_livro'),
    path('livro/ajax/<int:id_livro>/', views.ajax_detalhar_livro, name='ajax_detalhar_livro'),
    
    # CRUD Livros
    path('livros/cadastrar/', views.cadastro_livro, name='cadastro_livro'),
    path('livros/editar/<int:id_livro>/', views.editar_livro, name='editar_livro'),
    path('livros/deletar/<int:id_livro>/', views.deletar_livro, name='deletar_livro'),
    path('livros/gerenciar/', views.gerenciar_livros, name='gerenciar_livros'),
    
    # Empréstimos
    path('meus-emprestimos/', views.ver_emprestimos, name='ver_emprestimos'),
    path('meus-emprestimos/renovar/<int:id_emprestimo>/', views.renovar_meu_emprestimo, name='renovar_meu_emprestimo'),
    
    # CRUD Empréstimos (admin)
    path('emprestimos/cadastrar/', views.cadastro_emprestimo, name='cadastro_emprestimo'),
    path('emprestimos/editar/<int:id_emprestimo>/', views.editar_emprestimo, name='editar_emprestimo'),
    path('emprestimos/deletar/<int:id_emprestimo>/', views.deletar_emprestimo, name='deletar_emprestimo'),
    path('emprestimos/gerenciar/', views.gerenciar_emprestimos, name='gerenciar_emprestimos'),
    path('emprestimos/marcar-devolvido/<int:id_emprestimo>/', views.marcar_devolvido, name='marcar_devolvido'),
    path('emprestimos/renovar/<int:id_emprestimo>/', views.renovar_emprestimo, name='renovar_emprestimo'),
    
    # Gerenciamento de Usuários (admin)
    path('usuarios/gerenciar/', views.gerenciar_usuarios, name='gerenciar_usuarios'),
    path('usuarios/editar/<int:id_usuario>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/deletar/<int:id_usuario>/', views.deletar_usuario, name='deletar_usuario'),
    path('usuarios/toggle-status/<int:id_usuario>/', views.toggle_usuario_status, name='toggle_usuario_status'),
    path('usuarios/promover/<int:id_usuario>/', views.promover_usuario, name='promover_usuario'),
    path('usuarios/rebaixar/<int:id_usuario>/', views.rebaixar_usuario, name='rebaixar_usuario'),
    
    # Perfil do usuário
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    
    # Utilitários
    path('ajax/livros/', views.ajax_livros, name='ajax_livros'),
    path('ajax/mensagens/', views.ajax_mensagens, name='ajax_mensagens'),
    
    # Reset de senha (opcional)
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), 
         name='password_reset_complete'),
]

# Serve arquivos de mídia durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)