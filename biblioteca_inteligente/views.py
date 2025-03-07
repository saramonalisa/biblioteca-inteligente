from django.shortcuts import render, redirect, get_object_or_404
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from .models import Livro, Emprestimo
from .forms import LivroForm, EmprestimoForm, UserCreationForm
import time 

def index(request):
    if request.user.is_authenticated:
        return redirect('inicio') 
    return render(request, "index.html")

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
    livros_list = Livro.objects.all().order_by("titulo")
    pesquisa = request.GET.get("q")
    if pesquisa:
        livros_autor = Livro.objects.filter(autor__icontains=pesquisa)
        livros_titulo = Livro.objects.filter(titulo__icontains=pesquisa)
        livros_sinopse = Livro.objects.filter(sinopse__icontains=pesquisa)
        livros_list = livros_autor | livros_titulo | livros_sinopse
        livros_list = livros_list.distinct()

    paginator = Paginator(livros_list, 9)  # Mostra 9 livros por página
    page_number = request.GET.get('page')
    livros_paginados = paginator.get_page(page_number)
    return render(request, 'inicio.html', {'livros_paginados': livros_paginados})

def ajax_livros(request):
    time.sleep(2)
    livros_list = Livro.objects.all().order_by("titulo")
    pesquisa = request.GET.get("q")
    if pesquisa:
        livros_autor = Livro.objects.filter(autor__icontains=pesquisa)
        livros_titulo = Livro.objects.filter(titulo__icontains=pesquisa)
        livros_sinopse = Livro.objects.filter(sinopse__icontains=pesquisa)
        livros_list = livros_autor | livros_titulo | livros_sinopse
        livros_list = livros_list.distinct()
    paginator = Paginator(livros_list, 9)  # Mostra 9 livros por página
    page_number = request.GET.get('page')
    livros_paginados = paginator.get_page(page_number) # Pega a página específica
    return render(request, "inicio.html", {'livros_paginados': livros_paginados})

@login_required
def detalhar_livro(request, id_livro):
    livro = get_object_or_404(Livro, pk=id_livro)
    return render(request, "detalhar_livro.html", {"livro": livro})

@login_required
def ajax_detalhar_livro(request, id_livro):
    livro = get_object_or_404(Livro, pk=id_livro)
    return render(request, "partials/_card_livro.html", {"livro": livro})

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
@permission_required('biblioteca_inteligente.delete_livro')
def deletar_livro(request, id_livro):
    livro = get_object_or_404(Livro, pk=id_livro)
    if request.method == "POST":
        livro.delete()
        messages.success(request, "Livro removido com sucesso!")
        return redirect("gerenciar_livros")
    else:
        return render(request, "deletar_livro.html", {'livro': livro})

@login_required
@permission_required('app.edit_livro', raise_exception=True)
def editar_livro(request, id_livro):
    livro = get_object_or_404(Livro, pk=id_livro)
    if request.method == "POST":
        form = LivroForm(request.POST, request.FILES, instance=livro)
        if form.is_valid():
            form.save()
            messages.success(request, "Livro atualizado!")
            return redirect("gerenciar_livros")
        else:
            messages.error(request, "Falha ao criar livro!")
    else:
        form = LivroForm(instance=livro)
    return render(request, "editar_livro.html", {"form": form})

@login_required
@permission_required('app.change_emprestimo', raise_exception=True)
def editar_emprestimo(request, id):
    emprestimo = get_object_or_404(Livro, pk=id)
    if request.method == 'POST':
        form = LivroForm(request.POST, instance=emprestimo)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = LivroForm(instance=emprestimo)
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
@permission_required('biblioteca_inteligente.view_emprestimo')
def gerenciar_emprestimos(request):
    context = {
        "emprestimos": Emprestimo.objects.all()
    }
    return render(request, "gerenciar_emprestimos.html", context)

@login_required
@permission_required('biblioteca_inteligente.change_emprestimo')
def marcar_devolvido(request, id):
    emprestimo = get_object_or_404(Emprestimo, id=id)
    emprestimo.devolvido = True
    emprestimo.save()
    return HttpResponseRedirect(reverse('ver_emprestimos'))

@login_required
@permission_required('biblioteca_inteligente.view_livro')
def gerenciar_livros(request):
    context = {
        "livros": Livro.objects.all(),
    }
    return render(request, "gerenciar_livros.html", context)

def ajax_mensagens(request):
    messages = get_messages(request)
    return render(request, 'partials/_messages.html', {'messages': messages})
