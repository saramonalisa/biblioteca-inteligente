from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_user_model
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from .models import Livro, Emprestimo
from .forms import LivroForm, EmprestimoForm, CustomUserCreationForm, UserEditForm  # REMOVI UsuarioForm
from django.db.models import Q, Count
from datetime import date, timedelta
import time 

User = get_user_model()

def index(request):
    if request.user.is_authenticated:
        return redirect('inicio') 
    return render(request, "index.html")

def cadastro(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                # Configurar o email e nome do usuário
                user.email = form.cleaned_data.get('email')
                user.save()
                
                # Atualizar os campos adicionais no modelo User
                user.nome = form.cleaned_data.get('nome')
                user.telefone = form.cleaned_data.get('telefone')
                user.save()
                
                messages.success(request, f"Usuário {user.username} criado com sucesso! Faça login para acessar o sistema.")
                return redirect('login')
            except Exception as e:
                messages.error(request, f"Erro ao criar usuário: {str(e)}")
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/cadastro.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    messages.success(request, f"Bem-vindo, {user.nome or user.username}!")
                    if user.is_staff:
                        return redirect('inicio')
                    else:
                        return redirect('inicio')
                else:
                    messages.error(request, "Esta conta está desativada.")
            else:
                messages.error(request, "Usuário ou senha incorretos.")
        else:
            messages.error(request, "Usuário ou senha incorretos.")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})

def logout_view(request):
    auth_logout(request)
    messages.success(request, "Você saiu do sistema.")
    return redirect('index')

@login_required
def inicio(request):
    livros_list = Livro.objects.all().order_by("titulo")
    pesquisa = request.GET.get("q")
    if pesquisa:
        livros_list = Livro.objects.filter(
            Q(autor__icontains=pesquisa) |
            Q(titulo__icontains=pesquisa) |
            Q(sinopse__icontains=pesquisa) |
            Q(genero__icontains=pesquisa) |
            Q(editora__name__icontains=pesquisa)  # Correto para ManyToManyField
        ).distinct()

    # Verificar disponibilidade
    for livro in livros_list:
        livro.disponivel = livro.esta_disponivel()

    paginator = Paginator(livros_list, 9)
    page_number = request.GET.get('page')
    livros_paginados = paginator.get_page(page_number)
    
    # Passar as opções de gênero para o template
    generos = Livro.GENEROS
    
    return render(request, 'inicio.html', {
        'livros_paginados': livros_paginados,
        'generos': generos.items(),  # Passa como lista de tuplas
    })

def ajax_livros(request):
    time.sleep(2)
    livros_list = Livro.objects.all().order_by("titulo")
    pesquisa = request.GET.get("q")
    if pesquisa:
        livros_list = Livro.objects.filter(
            Q(autor__icontains=pesquisa) |
            Q(titulo__icontains=pesquisa) |
            Q(sinopse__icontains=pesquisa) |
            Q(genero__icontains=pesquisa) |
            Q(editora__name__icontains=pesquisa)
        ).distinct()
    
    # Verificar disponibilidade
    for livro in livros_list:
        livro.disponivel = livro.esta_disponivel()
    
    paginator = Paginator(livros_list, 9)
    page_number = request.GET.get('page')
    livros_paginados = paginator.get_page(page_number)
    return render(request, "partials/_livros_grid.html", {'livros_paginados': livros_paginados})

@login_required
def detalhar_livro(request, id_livro):
    livro = get_object_or_404(Livro, pk=id_livro)
    livro.disponivel = livro.esta_disponivel()
    return render(request, "detalhar_livro.html", {"livro": livro})

@login_required
def ajax_detalhar_livro(request, id_livro):
    livro = get_object_or_404(Livro, pk=id_livro)
    livro.disponivel = livro.esta_disponivel()
    return render(request, "partials/_card_livro.html", {"livro": livro})

# ============ CRUD LIVROS ============

@login_required
@user_passes_test(lambda u: u.is_staff)
def cadastro_livro(request):
    if request.method == 'POST':
        form = LivroForm(request.POST, request.FILES)
        if form.is_valid():
            livro = form.save()
            form.save_m2m()  # Salvar as relações many-to-many
            messages.success(request, f'Livro "{livro.titulo}" cadastrado com sucesso!')
            return redirect('gerenciar_livros')
        else:
            messages.error(request, 'Erro ao cadastrar livro. Verifique os campos.')
    else:
        form = LivroForm()
    return render(request, 'cadastro_livro.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def editar_livro(request, id_livro):
    livro = get_object_or_404(Livro, pk=id_livro)
    if request.method == "POST":
        form = LivroForm(request.POST, request.FILES, instance=livro)
        if form.is_valid():
            livro = form.save()
            form.save_m2m()  # Salvar as relações many-to-many
            messages.success(request, f'Livro "{livro.titulo}" atualizado com sucesso!')
            return redirect("gerenciar_livros")
        else:
            messages.error(request, "Falha ao atualizar livro!")
    else:
        form = LivroForm(instance=livro)
    return render(request, "editar_livro.html", {"form": form, "livro": livro})

@login_required
@user_passes_test(lambda u: u.is_staff)
def deletar_livro(request, id_livro):
    livro = get_object_or_404(Livro, pk=id_livro)
    
    # Verificar se o livro está emprestado
    emprestimos_ativos = Emprestimo.objects.filter(livro=livro, devolvido=False)
    
    if request.method == "POST":
        if emprestimos_ativos.exists():
            messages.error(request, f'Não é possível excluir "{livro.titulo}" pois está emprestado.')
            return redirect('gerenciar_livros')
        
        titulo = livro.titulo
        livro.delete()
        messages.success(request, f'Livro "{titulo}" removido com sucesso!')
        return redirect("gerenciar_livros")
    
    context = {
        'livro': livro,
        'tem_emprestimos': emprestimos_ativos.exists(),
    }
    return render(request, "deletar_livro.html", context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def gerenciar_livros(request):
    livros = Livro.objects.all().order_by('titulo')
    
    # Contagem de estatísticas
    total_livros = livros.count()
    livros_disponiveis = sum(1 for livro in livros if livro.esta_disponivel())
    livros_emprestados = total_livros - livros_disponiveis
    
    # Adicionar informação de disponibilidade
    for livro in livros:
        livro.disponivel = livro.esta_disponivel()
    
    context = {
        "livros": livros,
        "total_livros": total_livros,
        "livros_disponiveis": livros_disponiveis,
        "livros_emprestados": livros_emprestados,
    }
    return render(request, "gerenciar_livros.html", context)

# ============ CRUD EMPRÉSTIMOS ============

@login_required
@user_passes_test(lambda u: u.is_staff)
def cadastro_emprestimo(request):
    if request.method == "POST":
        form = EmprestimoForm(request.POST)
        if form.is_valid():
            emprestimo = form.save(commit=False)
            
            # Definir data atual
            emprestimo.data = date.today()
            
            # Definir data de devolução padrão (15 dias)
            if not emprestimo.data_devolucao:
                emprestimo.data_devolucao = date.today() + timedelta(days=15)
            
            emprestimo.save()
            form.save_m2m()  # Salvar relação many-to-many com livros
            
            messages.success(request, f'Empréstimo registrado com sucesso!')
            return redirect('gerenciar_emprestimos')
        else:
            messages.error(request, 'Erro ao registrar empréstimo. Verifique os campos.')
    else:
        # Definir data de devolução padrão
        data_devolucao_padrao = date.today() + timedelta(days=15)
        form = EmprestimoForm(initial={
            'data': date.today(),
            'data_devolucao': data_devolucao_padrao
        })
    
    return render(request, "cadastro_emprestimo.html", {"form": form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def editar_emprestimo(request, id_emprestimo):
    emprestimo = get_object_or_404(Emprestimo, pk=id_emprestimo)
    
    if request.method == 'POST':
        form = EmprestimoForm(request.POST, instance=emprestimo)
        if form.is_valid():
            emprestimo = form.save()
            form.save_m2m()  # Salvar relação many-to-many
            messages.success(request, f'Empréstimo atualizado com sucesso!')
            return redirect('gerenciar_emprestimos')
        else:
            messages.error(request, 'Erro ao atualizar empréstimo.')
    else:
        form = EmprestimoForm(instance=emprestimo)
    
    context = {
        'form': form,
        'emprestimo': emprestimo,
    }
    return render(request, 'editar_emprestimo.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def deletar_emprestimo(request, id_emprestimo):
    emprestimo = get_object_or_404(Emprestimo, pk=id_emprestimo)
    
    if request.method == "POST":
        # Obter títulos dos livros para a mensagem
        livros = [livro.titulo for livro in emprestimo.livro.all()]
        emprestimo.delete()
        
        messages.success(request, f'Empréstimo de {", ".join(livros[:2])} removido com sucesso!')
        return redirect("gerenciar_emprestimos")
    
    context = {
        'emprestimo': emprestimo,
        'livros': emprestimo.livro.all(),
    }
    return render(request, "deletar_emprestimo.html", context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def gerenciar_emprestimos(request):
    emprestimos = Emprestimo.objects.all().order_by('-data')
    
    # Filtros
    status = request.GET.get('status')
    if status == 'pendente':
        emprestimos = emprestimos.filter(devolvido=False)
    elif status == 'devolvido':
        emprestimos = emprestimos.filter(devolvido=True)
    
    # Adicionar informações extras
    for emp in emprestimos:
        emp.atrasado = emp.esta_atrasado()
        emp.dias_atrasado = emp.dias_de_atraso() if emp.atrasado else 0
    
    # Contagem por status
    total_emprestimos = emprestimos.count()
    emprestimos_devolvidos = emprestimos.filter(devolvido=True).count()
    emprestimos_pendentes = total_emprestimos - emprestimos_devolvidos
    emprestimos_atrasados = sum(1 for emp in emprestimos if emp.atrasado and not emp.devolvido)
    
    context = {
        "emprestimos": emprestimos,
        "total_emprestimos": total_emprestimos,
        "emprestimos_devolvidos": emprestimos_devolvidos,
        "emprestimos_pendentes": emprestimos_pendentes,
        "emprestimos_atrasados": emprestimos_atrasados,
    }
    return render(request, "gerenciar_emprestimos.html", context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def marcar_devolvido(request, id_emprestimo):
    emprestimo = get_object_or_404(Emprestimo, pk=id_emprestimo)
    
    if not emprestimo.devolvido:
        emprestimo.devolvido = True
        emprestimo.save()
        messages.success(request, f'Livro(s) marcado(s) como devolvido(s) com sucesso!')
    else:
        messages.warning(request, 'Este empréstimo já está marcado como devolvido.')
    
    return HttpResponseRedirect(reverse('gerenciar_emprestimos'))

@login_required
@user_passes_test(lambda u: u.is_staff)
def renovar_emprestimo(request, id_emprestimo):
    emprestimo = get_object_or_404(Emprestimo, pk=id_emprestimo)
    
    if request.method == "POST":
        # Adicionar 7 dias à data de devolução
        if emprestimo.data_devolucao:
            emprestimo.data_devolucao += timedelta(days=7)
            emprestimo.save()
            messages.success(request, 'Empréstimo renovado por mais 7 dias!')
        else:
            messages.error(request, 'Não foi possível renovar o empréstimo.')
    
    return HttpResponseRedirect(reverse('gerenciar_emprestimos'))

# ============ VISUALIZAÇÃO DO USUÁRIO ============

@login_required
def ver_emprestimos(request):
    emprestimos = Emprestimo.objects.filter(usuario=request.user).order_by('-data')
    
    # Adicionar informações extras
    for emp in emprestimos:
        emp.atrasado = emp.esta_atrasado()
        emp.dias_atrasado = emp.dias_de_atraso()
    
    # Contagens
    total = emprestimos.count()
    devolvidos = emprestimos.filter(devolvido=True).count()
    pendentes = total - devolvidos
    atrasados = sum(1 for emp in emprestimos if emp.atrasado and not emp.devolvido)
    
    context = {
        "emprestimos": emprestimos,
        "emprestimos_devolvidos": devolvidos,
        "emprestimos_pendentes": pendentes,
        "emprestimos_atrasados": atrasados,
    }
    return render(request, "ver_emprestimos.html", context)

@login_required
def renovar_meu_emprestimo(request, id_emprestimo):
    emprestimo = get_object_or_404(Emprestimo, pk=id_emprestimo, usuario=request.user)
    
    if not emprestimo.devolvido and emprestimo.data_devolucao:
        # Verificar se não está atrasado
        if not emprestimo.esta_atrasado():
            emprestimo.data_devolucao += timedelta(days=7)
            emprestimo.save()
            messages.success(request, 'Empréstimo renovado por mais 7 dias!')
        else:
            messages.error(request, 'Não é possível renovar um empréstimo atrasado.')
    else:
        messages.error(request, 'Não foi possível renovar este empréstimo.')
    
    return HttpResponseRedirect(reverse('ver_emprestimos'))

# ============ CRUD USUÁRIOS ============

@login_required
@user_passes_test(lambda u: u.is_staff)
def gerenciar_usuarios(request):
    usuarios = User.objects.all().order_by('-date_joined')
    
    # Contar estatísticas
    total_usuarios = usuarios.count()
    usuarios_ativos = usuarios.filter(is_active=True).count()
    usuarios_staff = usuarios.filter(is_staff=True).count()
    usuarios_superuser = usuarios.filter(is_superuser=True).count()
    usuarios_regulares = total_usuarios - usuarios_staff - usuarios_superuser
    
    context = {
        "usuarios": usuarios,
        "total_usuarios": total_usuarios,
        "usuarios_ativos": usuarios_ativos,
        "usuarios_staff": usuarios_staff,
        "usuarios_superuser": usuarios_superuser,
        "usuarios_regulares": usuarios_regulares,
    }
    return render(request, "gerenciar_usuarios.html", context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def editar_usuario(request, id_usuario):
    usuario = get_object_or_404(User, pk=id_usuario)
    
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, f'Usuário {usuario.username} atualizado com sucesso!')
            return redirect('gerenciar_usuarios')
        else:
            messages.error(request, 'Erro ao atualizar usuário.')
    else:
        form = UserEditForm(instance=usuario)
    
    return render(request, "editar_usuario.html", {
        "form": form,
        "usuario": usuario
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def deletar_usuario(request, id_usuario):
    usuario = get_object_or_404(User, pk=id_usuario)
    
    if request.method == "POST":
        if usuario == request.user:
            messages.error(request, 'Você não pode excluir sua própria conta!')
        else:
            username = usuario.username
            usuario.delete()
            messages.success(request, f'Usuário {username} removido com sucesso!')
        return redirect("gerenciar_usuarios")
    
    return render(request, "deletar_usuario.html", {'usuario': usuario})

@login_required
@user_passes_test(lambda u: u.is_staff)
def toggle_usuario_status(request, id_usuario):
    usuario = get_object_or_404(User, pk=id_usuario)
    
    if usuario != request.user:
        usuario.is_active = not usuario.is_active
        usuario.save()
        
        status = "ativado" if usuario.is_active else "desativado"
        messages.success(request, f'Usuário {usuario.username} {status} com sucesso!')
    else:
        messages.error(request, 'Você não pode alterar seu próprio status!')
    
    return HttpResponseRedirect(reverse('gerenciar_usuarios'))

@login_required
@user_passes_test(lambda u: u.is_staff)
def promover_usuario(request, id_usuario):
    usuario = get_object_or_404(User, pk=id_usuario)
    
    if usuario != request.user:
        usuario.is_staff = True
        usuario.save()
        messages.success(request, f'Usuário {usuario.username} promovido a administrador!')
    else:
        messages.error(request, 'Ação não permitida.')
    
    return HttpResponseRedirect(reverse('gerenciar_usuarios'))

@login_required
@user_passes_test(lambda u: u.is_staff)
def rebaixar_usuario(request, id_usuario):
    usuario = get_object_or_404(User, pk=id_usuario)
    
    if usuario != request.user:
        usuario.is_staff = False
        usuario.save()
        messages.success(request, f'Usuário {usuario.username} rebaixado a usuário regular.')
    else:
        messages.error(request, 'Você não pode rebaixar a si mesmo!')
    
    return HttpResponseRedirect(reverse('gerenciar_usuarios'))

@login_required
def perfil_usuario(request):
    usuario = request.user
    
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil_usuario')
        else:
            messages.error(request, 'Erro ao atualizar perfil.')
    else:
        # Remova campos is_staff e is_active para usuários comuns
        if not usuario.is_staff:
            form = UserEditForm(instance=usuario)
            # Remover campos administrativos
            form.fields.pop('is_staff', None)
            form.fields.pop('is_active', None)
        else:
            form = UserEditForm(instance=usuario)
    
    # Pegar estatísticas do usuário
    emprestimos = Emprestimo.objects.filter(usuario=usuario)
    total_emprestimos = emprestimos.count()
    emprestimos_ativos = emprestimos.filter(devolvido=False).count()
    
    return render(request, "perfil_usuario.html", {
        "form": form,
        "total_emprestimos": total_emprestimos,
        "emprestimos_ativos": emprestimos_ativos,
    })

# ============ UTILITÁRIOS ============

def ajax_mensagens(request):
    messages = get_messages(request)
    return render(request, 'partials/_messages.html', {'messages': messages})
