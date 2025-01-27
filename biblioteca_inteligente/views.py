from django.shortcuts import render, redirect, get_object_or_404
from django.forms.models import model_to_dict
from .models import Livro, Emprestimo
from .forms import CadastroForm, LivroForm, EmprestimoForm
from django.contrib.auth.decorators import login_required

def index(request):
    context = {}
    return render(request, "index.html", context)

def cadastro(request):
    context = {}
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    
    return render(request, 'cadastro.html', context)

@login_required
def inicio(request):
    context = {}
    return render(request, "inicio.html", context)

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

def catalogo(request):
    context = {
        "livro": Livro.objects.all()
    }
    return render(request, "catalogo.html", context)

def ver_emprestimos(request):
    context = {
        "emprestimo": Emprestimo.objects.all()
    }
    return render(request, "ver_emprestimos.html", context)

def configuracoes(request):
    context = {}
    return render(request, "configuracoes.html", context)