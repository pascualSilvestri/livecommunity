from django.db import models
from django.conf import settings


class Cliente(models.Model):
    idCliente = models.TextField(max_length=50)
    nombre = models.TextField(max_length=200)
    url = models.URLField()
    
    def __str__(self):
        return self.nombre
    
    
    