from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    matricula = models.CharField(max_length=20)
    telefone = models.CharField(max_length=14)
    def __str__(self):
        return self.username

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='media/')

    def __str__(self):
        return self.usuario.username

