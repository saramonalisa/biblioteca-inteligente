from django.shortcuts import render, redirect, get_object_or_404
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.core.paginator import Paginator
from datetime import timedelta
from .models import Livro, Emprestimo
from .forms import LivroForm, EmprestimoForm, CadastroForm

def index(request):
    context = {}
    return render(request, "index.html", context)

def cadastro(request):
    if request.method == "POST":
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Usuário {username} criado com sucesso! Faça login para acessar o sistema.")
            return redirect('login')
    else:
        form = CadastroForm()
    return render(request, "registration/cadastro.html", {"form": form})

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f"Bem-vindo, {nome}!")
                return redirect('index')
            else:
                messages.error(request, "Usuário ou senha incorretos.")
        else:
            messages.error(request, "Usuário ou senha incorretos.")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})

def editar_perfil(request):
    if request.method == "POST":
        form = UsuarioChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado!")
            return redirect("perfil")
        else:
            messages.success(request, "Falha ao atualizar o perfil!")
    else:
        form = UsuarioChangeForm(instance=request.user)

    return render(request, "registration/editar_perfil.html", {"form": form})

@login_required
def inicio(request):
    livros = Livro.objects.all().order_by("?")[:9]
    return render(request, "inicio.html", {"livros": livros})

def livros(request):
    filtro = request.GET.get("f")
    if filtro and filtro in Livro.GENEROS:
        livros = Livro.objects.filter(genero=filtro).order_by("id")
    else:
        livros = Livro.objects.all().order_by("id")
    paginator = Paginator(livros, 6)
    numero_da_pagina = request.GET.get('p')  # Pega o número da página da URL
    livros_paginados = paginator.get_page(numero_da_pagina)  # Pega a página específica
    return render(request, "biblioteca/livros.html", {"livros": livros_paginados, "opcoes": Livro.GENEROS.items()})

def detalhar_livro(request, id_livro):
    livro = get_object_or_404(Livro, id=id_livro)
    return render(request, "biblioteca/detalhar_livro.html", {"livro": livro})

def pesquisa(request):
    pesquisa = request.GET.get("q")
    if pesquisa:
        livros_autor = Livro.objects.filter(autor__icontains=pesquisa)
        livros_titulo = Livro.objects.filter(titulo__icontains=pesquisa)
        livros_sinopse = Livro.objects.filter(sinopse__icontains=pesquisa)
        livros = livros_autor | livros_titulo | livros_sinopse
        livros.distinct()
    
    paginator = Paginator(livros, 6)
    numero_da_pagina = request.GET.get('p')  # Pega o número da página da URL
    livros_paginados = paginator.get_page(numero_da_pagina)  # Pega a página específica
    return render(request, "biblioteca/pesquisa.html", {"livros": livros_paginados})

@login_required
@permission_required('biblioteca_inteligente.add_livro')
def cadastro_livro(request):
    context = {}

    if request.method == "POST":
        form = LivroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            context["form"] = form # esse é o form com os erros
    else:
        context["form"] = LivroForm()

    return render(request, "cadastro_livro.html", context)

@login_required
@permission_required('biblioteca_inteligente.add_emprestimo')
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
        "emprestimos": Emprestimo.objects.all()
    }
    return render(request, "ver_emprestimos.html", context)

@login_required
def configuracoes(request):
    context = {}
    return render(request, "configuracoes.html", context)