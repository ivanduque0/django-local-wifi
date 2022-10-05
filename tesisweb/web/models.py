from enum import unique
from django.db import models  
# Create your models here.
class usuarios(models.Model):
    cedula = models.CharField(max_length=150,primary_key=False)
    nombre = models.CharField(max_length=150)
    id_usuario = models.CharField(max_length=150, blank=True) 
    
    class Meta:
        verbose_name_plural = "Usuarios"

class interacciones(models.Model):
    nombre = models.CharField(max_length=150)
    fecha = models.DateField()
    hora = models.TimeField()
    razon = models.CharField(max_length=150)
    contrato = models.CharField(max_length=100)
    cedula = models.CharField(max_length=150)
    class Meta:
        verbose_name_plural = "Interacciones"

class horariospermitidos(models.Model):

    class dias(models.TextChoices):
        LUNES = 'Lunes', 'Lunes'
        MARTES = 'Martes', 'Martes'
        MIERCOLES = 'Miercoles','Miercoles'
        JUEVES = 'Jueves', 'Jueves'
        VIERNES = 'Viernes', 'Viernes'
        SABADO = 'Sabado', 'Sabado'
        DOMINGO = 'Domingo', 'Domingo'
        SIEMPRE = 'Siempre', 'Siempre'

    # en este campo se debe poner el "id" del usuario, no la cedula
    dia=models.CharField(max_length=20, choices=dias.choices)
    entrada=models.TimeField()
    salida=models.TimeField()
    cedula = models.CharField(max_length=150)
    class Meta:
        verbose_name_plural = "Horarios"

# class apertura(models.Model):
#     acceso = models.CharField(max_length=50)
#     id_usuario = models.CharField(max_length=150)
#     cedula = serializers.CharField()
#     id_usuario = serializers.CharField()