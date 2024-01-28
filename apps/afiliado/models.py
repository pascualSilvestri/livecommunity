from django.db import models
from django.conf import settings



class Afiliado(models.Model):
    fpa = models.CharField(max_length=50)
    url = models.URLField()
    url_video = models.URLField(default="https://www.youtube.com/watch?v=HgKjhFEguy")
    upline = models.CharField(max_length=50)
    
    def __str__(self):
        return self.fpa
    
    
class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    correo = models.EmailField()
    telefono = models.BigIntegerField()
    idAfiliado = models.CharField(max_length=50)
    userTelegram = models.CharField(max_length=200)
    idCliente = models.CharField(max_length=50) #Recibir parametro por input


    def __str__(self):
        return self.nombre
    
