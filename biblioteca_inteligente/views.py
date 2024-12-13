from django.shortcuts import render, redirect, get_object_or_404
from django.forms.models import model_to_dict

def index(request):
    context = {}
    return render(request, "index.html", context)

def cadastro(request):
    context = {}
    return render(request, "cadastro.html", context)