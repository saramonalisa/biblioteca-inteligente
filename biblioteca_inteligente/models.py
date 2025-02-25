from django import forms
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

class Usuario(AbstractUser):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=14)

    def __str__(self):
        return self.username

class Editora(models.Model):
    editora = models.CharField(max_length=100)
    
    def __str__(self):
        return self.editora
    
class Livro(models.Model):
    LIVRE = "LI"
    MAIORES_10 = "10"
    MAIORES_12 = "12"
    MAIORES_14 = "14"
    MAIORES_16 = "16"
    MAIORES_18 = "18"
    CLASSIFICACOES = {
        LIVRE: "Livre",
        MAIORES_10: "10 anos",
        MAIORES_12: "12 anos",
        MAIORES_14: "14 anos",
        MAIORES_16: "16 anos",
        MAIORES_18: "18 anos",
        }
    
    ROMANCE = "RO"
    BIOGRAFIA = "BI"
    TECNICO = "TE"
    FICCAO = "FI"
    FANTASIA = "FA"
    MISTERIO = "MI"
    POESIA = "PO"
    DRAMA = "DR"
    TERROR = "HO"
    AVENTURA = "AD"
    INFANTIL = "CH"
    JOVEM_ADULTO = "YA"
    FICCAO_CIENTIFICA = "SF"
    OUTROS = "OU"

    GENEROS = {
        ROMANCE: "Romance",
        BIOGRAFIA: "Biografia",
        TECNICO: "Técnico",
        FICCAO: "Ficção",
        FANTASIA: "Fantasia",
        MISTERIO: "Mistério",
        POESIA: "Poesia",
        DRAMA: "Drama",
        TERROR: "Terror",
        AVENTURA: "Aventura",
        INFANTIL: "Infantil",
        JOVEM_ADULTO: "Jovem Adulto",
        FICCAO_CIENTIFICA: "Ficção Científica",
        OUTROS: "Outros",
    }
    
    titulo = models.CharField(max_length=150)
    autor = models.CharField(max_length=100)
    capa = models.ImageField(upload_to="livros/capas/", blank=True)
    editora = models.ManyToManyField(Editora)
    isbn = models.CharField(max_length=13)
    publicacao = models.IntegerField(blank=True)
    classificacao = models.CharField(max_length=2, choices=CLASSIFICACOES)
    genero = models.CharField(max_length=2, choices=GENEROS)
    sinopse = models.TextField(max_length=4000)
    
    def __str__(self):
        return self.titulo
    
class Emprestimo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    livro = models.ManyToManyField(Livro)
    data = models.DateField(auto_now_add=True)
    devolvido = models.BooleanField(default=False)
    
    def __str__(self):
        livros = ', '.join([livro.titulo for livro in self.livro.all()])
        return f'{self.usuario.username} | {livros} | {self.data}'
    
    @property
    def data_devolucao(self):
        return self.data + datetime.timedelta(days=15)