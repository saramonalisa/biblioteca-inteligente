from django.shortcuts import render, redirect, get_object_or_404
from django.forms.models import model_to_dict
from .models import Usuario, Livro, Emprestimo
from .forms import UserForm, LivroForm, EmprestimoForm
from django.contrib.auth.decorators import login_required

def index(request):
    context = {}
    return render(request, "index.html", context)

def inicio(request):
    context = {}
    return render(request, "inicio.html", context)

def cadastro(request):
    context = {}
    return render(request, "cadastro.html", context)

def cadastro_livro(request):
    context = {}
    return render(request, "cadastro_livro.html", context)

def cadastro_emprestimo(request):
    context = {}
    return render(request, "cadastro_emprestimo.html", context)

def catalogo(request):
    context = {}
    return render(request, "catalogo.html", context)

def ver_emprestimos(request):
    context = {}
    return render(request, "ver_emprestimos.html", context)

def configuracoes(request):
    context = {}
    return render(request, "configuracoes.html", context)