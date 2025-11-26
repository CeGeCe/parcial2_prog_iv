from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.IntegerField(unique=True) # Campo único para evitar duplicados
    email = models.EmailField(blank=True)
    
    # Relación con el usuario (Profesor) que lo creó
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.apellido}, {self.nombre}"