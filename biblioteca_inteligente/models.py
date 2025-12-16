from django import forms
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date, timedelta

class Usuario(AbstractUser):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=14)

    def __str__(self):
        return self.username

    @property
    def emprestimos_ativos(self):
        """Retorna os empréstimos ativos do usuário"""
        return self.emprestimo_set.filter(devolvido=False)

    @property
    def total_emprestimos(self):
        """Retorna o total de empréstimos do usuário"""
        return self.emprestimo_set.count()

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
    capa = models.ImageField(upload_to="livros/capas/", blank=True, null=True)
    editora = models.ManyToManyField(Editora)
    isbn = models.CharField(max_length=13)
    publicacao = models.IntegerField(blank=True, null=True)
    classificacao = models.CharField(max_length=2, choices=CLASSIFICACOES)
    genero = models.CharField(max_length=2, choices=GENEROS)
    sinopse = models.TextField(max_length=4000, blank=True, null=True)
    quantidade = models.IntegerField(default=1)
    
    def __str__(self):
        return self.titulo
    
    def esta_disponivel(self):
        """Verifica se o livro está disponível para empréstimo"""
        emprestimos_ativos = self.emprestimo_set.filter(devolvido=False).count()
        return emprestimos_ativos < self.quantidade
    
    @property
    def disponibilidade(self):
        """Retorna a disponibilidade como string"""
        return "Disponível" if self.esta_disponivel() else "Indisponível"
    
    def get_quantidade_disponivel(self):
        """Retorna quantas cópias estão disponíveis"""
        emprestimos_ativos = self.emprestimo_set.filter(devolvido=False).count()
        return max(0, self.quantidade - emprestimos_ativos)
    
    @property
    def editoras_str(self):
        """Retorna as editoras como string separada por vírgulas"""
        return ', '.join([e.editora for e in self.editora.all()])
    
class Emprestimo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    livro = models.ManyToManyField(Livro)
    data = models.DateField(auto_now_add=True)
    data_devolucao = models.DateField(blank=True, null=True)
    devolvido = models.BooleanField(default=False)
    
    def __str__(self):
        livros = ', '.join([livro.titulo for livro in self.livro.all()[:3]])
        if self.livro.count() > 3:
            livros += f'... (+{self.livro.count() - 3})'
        return f'{self.usuario.username} | {livros} | {self.data}'
    
    def save(self, *args, **kwargs):
        """Define data_devolucao padrão se não for fornecida"""
        if not self.data_devolucao:
            self.data_devolucao = date.today() + timedelta(days=15)
        super().save(*args, **kwargs)
    
    def esta_atrasado(self):
        """Verifica se o empréstimo está atrasado"""
        if self.devolvido:
            return False
        if self.data_devolucao:
            return self.data_devolucao < date.today()
        return False
    
    @property
    def status(self):
        """Retorna o status do empréstimo"""
        if self.devolvido:
            return "Devolvido"
        elif self.esta_atrasado():
            return "Atrasado"
        else:
            return "Pendente"
    
    def dias_de_atraso(self):
        """Retorna o número de dias de atraso"""
        if self.esta_atrasado() and self.data_devolucao:
            return (date.today() - self.data_devolucao).days
        return 0
    
    def renovar(self, dias=7):
        """Renova o empréstimo por mais dias"""
        if not self.devolvido and self.data_devolucao:
            self.data_devolucao += timedelta(days=dias)
            self.save()
            return True
        return False