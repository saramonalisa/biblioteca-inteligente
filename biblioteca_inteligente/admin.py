from django.contrib import admin
from .models import Livro, Genero, Classificacao, Editora

admin.site.register(Editora)
admin.site.register(Livro)
admin.site.register(Genero)
admin.site.register(Classificacao)