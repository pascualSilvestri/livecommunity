from django.db import models
from django.conf import settings


class Afiliado(models.Model):
    idAfiliado = models.CharField(max_length=50)
    nombre = models.CharField(max_length=200)
    url = models.URLField()
    
    def __str__(self):
        return self.nombre
    
    
class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    correo = models.EmailField()
    telefono = models.IntegerField()
    comprobante = models.ImageField(upload_to='comprobante')
    idAfiliado = models.CharField(max_length=50)


    def __str__(self):
        return self.nombre
    
