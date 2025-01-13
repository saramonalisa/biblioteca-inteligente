from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    
    
    def __str__(self):
        return self.titulo

class Editora(models.Model):
    editora = models.CharField(max_length=100)
    
    def __str__(self):
        return self.editora

class Classificacao(models.Model):
    classificacao = models.CharField()
    
    def __str__(self):
        return self.classificacao

class Genero(models.Model):
    genero = models.CharField()
    
    def __str__(self):
        return self.genero
    
class Livro(models.Model):
    titulo = models.CharField(max_length=150)
    autor = models.CharField(max_length=100)
    editora = models.ManyToManyField(Editora)
    isbn = models.CharField(max_length=13)
    publicacao = models.IntegerField()
    classificacao = models.ManyToManyField(Classificacao)
    genero = models.ManyToManyField(Genero)
    sinopse = models.TextField(max_length=4000)
    
    def __str__(self):
        return self.titulo
    
class Emprestimo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    livro = models.ManyToManyField(Livro)
    data = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.titulo