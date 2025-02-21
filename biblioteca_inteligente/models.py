from django.db import models

from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20)
    telefone = models.CharField(max_length=14)
    avatar = models.ImageField(
        upload_to="usuarios/avatar/",
        blank=True,
        null=True,
    ) 

    def __str__(self):
        return self.first_name

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
    data = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.titulo