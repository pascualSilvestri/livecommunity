from django.db import models
from django.conf import settings



class Verificar(models.Model):
    id = models.CharField(max_length=50,primary_key=True)
    
    def __str__(self):
        return self.id
    
class Archivo(models.Model):
    archivo = models.FileField(upload_to='media')
    
