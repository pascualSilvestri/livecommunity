from django.db import models
from django.conf import settings



class Afiliado(models.Model):
    idAfiliado = models.CharField(max_length=50)
    nombre = models.CharField(max_length=200)
    url = models.URLField()
    telefono = models.BigIntegerField()
    referenciaAfiliado = models.ForeignKey('self', null=True, blank=True, on_delete= models.SET_NULL)
    
    def __str__(self):
        return self.nombre
    
    
class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    correo = models.EmailField()
    telefono = models.IntegerField()
    idAfiliado = models.CharField(max_length=50)
    userTelegram = models.CharField(max_length=200)
    idCliente = models.CharField(max_length=50) #Recibir parametro por input


    def __str__(self):
        return self.nombre
    
