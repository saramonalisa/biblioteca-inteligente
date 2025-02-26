from django.shortcuts import render, redirect, get_object_or_404
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from .models import Livro, Emprestimo
from .forms import LivroForm, EmprestimoForm, UserCreationForm

def index(request):
    context = {}
    return render(request, "index.html", context)

def cadastro(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Usuário {username} criado com sucesso! Faça login para acessar o sistema.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, "registration/cadastro.html", {"form": form})

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f"Bem-vindo, {username}!")
                return redirect('inicio')
            else:
                messages.error(request, "Usuário ou senha incorretos.")
        else:
            messages.error(request, "Usuário ou senha incorretos.")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})

@login_required
def inicio(request):
    livros = Livro.objects.all().order_by("?")[:9]
    pesquisa = request.GET.get("q")
    paginator = Paginator(livros, 6)
    numero_da_pagina = request.GET.get('p')  # Pega o número da página da URL
    livros_paginados = paginator.get_page(numero_da_pagina)
    if pesquisa:
        livros_autor = Livro.objects.filter(autor__icontains=pesquisa)
        livros_titulo = Livro.objects.filter(titulo__icontains=pesquisa)
        livros_sinopse = Livro.objects.filter(sinopse__icontains=pesquisa)
        livros = livros_autor | livros_titulo | livros_sinopse
        livros.distinct()
    return render(request, "inicio.html", {"livros": livros_paginados})

@login_required
def detalhar_livro(request, id_livro):
    livro = get_object_or_404(Livro, id=id_livro)
    return render(request, "livro.html", {"livro": livro})

@login_required
@permission_required('biblioteca_inteligente.add_livro', raise_exception=True)
def cadastro_livro(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Livro cadastrado com sucesso!')
            return redirect('inicio')
        else:
            messages.error(request, 'Erro ao cadastrar livro!')
    else:
        form = LivroForm()
    return render(request, 'cadastro_livro.html', {'form': form})

@login_required
@permission_required('biblioteca_inteligente.change_livro')
def deletar_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=id_livro)
    livro.delete()
    return render(request, "deletar_livro.html", context)

@login_required
@permission_required('app.change_livro', raise_exception=True)
def editar_livro(request, id_livro):
    livro = get_object_or_404(Livro, pk=id_livro)
    if request.method == 'POST':
        form = LivroForm(request.POST, instance=livro)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = LivroForm(instance=livro)
    return render(request, 'criar.html', {'form': form})

@login_required
@permission_required('biblioteca_inteligente.add_emprestimo', raise_exception=True)
def cadastro_emprestimo(request):
    context = {}

    if request.method == "POST":
        form = EmprestimoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            context["form"] = form # esse é o form com os erros
    else:
        context["form"] = EmprestimoForm()
    
    return render(request, "cadastro_emprestimo.html", context)

@login_required
def ver_emprestimos(request):
    context = {
        "emprestimos": Emprestimo.objects.filter(usuario=request.user)
    }
    return render(request, "ver_emprestimos.html", context)

@login_required
@permission_required
def gerenciar_emprestimos(request):
    context = {
        "emprestimos": Emprestimo.objects.all()
    }
    return render(request, "gerenciar_emprestimos.html", context)

@login_required
@permission_required('biblioteca_inteligente.change_emprestimo')
def marcar_devolvido(request, emprestimo_id):
    emprestimo = get_object_or_404(Emprestimo, id=emprestimo_id)
    emprestimo.devolvido = True
    emprestimo.save()
    return HttpResponseRedirect(reverse('ver_emprestimos'))