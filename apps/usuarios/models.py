from django.db import models
from django.contrib.auth.models import AbstractUser

class BonoCpa(models.Model):
    idBonoCPA=  models.AutoField('id', primary_key=True)
    bono= models.CharField(max_length=50)
    valor= models.IntegerField() 
    
    def __str__(self):
        return self.bono
    
class BonoCpaIndirecto(models.Model):
    idBonoCPA=  models.AutoField('id', primary_key=True)
    bono= models.CharField(max_length=50)
    valor= models.IntegerField() 
    
    def __str__(self):
        return self.bono

class Spread(models.Model):
    idSpread=  models.AutoField('id', primary_key=True)
    spread= models.CharField(max_length=50)
    porcentaje= models.FloatField() 
    
    def __str__(self):
        return self.spread
    
    
class Usuario(AbstractUser):
    # Agrega campos adicionales personalizados para tu modelo de usuario, por ejemplo:
    afiliadoid = models.CharField(max_length=50)
    telephone = models.CharField(max_length=15)
    wallet = models.CharField(max_length=100)
    uplink = models.CharField(max_length=50,null=True)
    link = models.CharField(max_length=100)
    cpa = models.IntegerField(default=0)
    cpaIndirecto = models.IntegerField(default=0)
    monto_total= models.FloatField(default=0.0)
    monto_a_pagar= models.FloatField(default=0.0)
    monto_directo= models.FloatField(default=0.0) 
    monto_indirecto= models.FloatField(default=0.0)
    monto_cpa= models.FloatField(default=0.0)
    monto_bono_directo= models.FloatField(default=0.0)
    monto_bono_indirecto= models.FloatField(default=0.0)
    retiros= models.FloatField(default=0.0)
    roles= models.CharField(max_length=50,default="user")
    aceptado= models.BooleanField(default=False)
    eliminado= models.BooleanField(default=False)
    haveBono= models.BooleanField(default=False)
    level_bono_directo=models.IntegerField(default=0)
    level_bono_indirecto=models.IntegerField(default=0)
    # bonoIndirecto_2=models.BooleanField(default=False)
    # bonoIndirecto_3=models.BooleanField(default=False)
    # bonoIndirecto_4=models.BooleanField(default=False)
    # bonoIndirecto_5=models.BooleanField(default=False)
    # bonoIndirecto_6=models.BooleanField(default=False)
    # bonoIndirecto_7=models.BooleanField(default=False)
    # bonoIndirecto_8=models.BooleanField(default=False)

    # Puedes agregar más campos personalizados según tus necesidades
    # ...

    def __str__(self):
        return self.afiliadoid

    
class PagoRealizado(models.Model):
    id_pagos= models.AutoField('id', primary_key=True)
    afiliadoid = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    monto_total=models.FloatField(default=0.0)
    monto_pagado= models.FloatField(default=0.0)
    monto_cpa= models.FloatField(default=0.0)
    monto_indirecto= models.FloatField(default=0.0)
    monto_bono_indirecto= models.FloatField(default=0.0)
    monto_bono_directo= models.FloatField(default=0.0)
    
    def __str__(self):
        return self.afiliadoid
