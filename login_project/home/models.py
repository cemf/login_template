from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Usuario(AbstractUser):
    endereco = models.TextField()

    def __str__(self):
        return self.usuario

    class Meta:
        db_table = 'usuarios'