from django.db import models

# Create your models here.
class Usuario(models.Model):
    usuario = models.CharField(max_length=100)
    login = models.CharField(max_length=50, unique=True)
    senha = models.CharField(max_length=100)
    endereco = models.TextField()

    def __str__(self):
        return self.usuario
