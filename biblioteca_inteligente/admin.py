from django.contrib import admin
from .models import Usuario, Livro, Editora, Emprestimo

admin.site.register(Editora)
admin.site.register(Livro)
admin.site.register(Usuario)
admin.site.register(Emprestimo)