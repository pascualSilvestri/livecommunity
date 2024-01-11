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
    
class CPA(models.Model):
    id=  models.AutoField('id', primary_key=True)
    cpa= models.FloatField()
    
    def __str__(self):
        return str(self.id)
    
class Broker(models.Model):
    idBroker=  models.AutoField('id', primary_key=True)
    broker= models.CharField(max_length=50)
    
    def __str__(self):
        return self.broker


class Usuario(AbstractUser):
    # Agrega campos adicionales personalizados para tu modelo de usuario, por ejemplo:
    uid = models.CharField(max_length=50,null=True)
    codigo_bingx = models.CharField(max_length=50,null=True)
    fpa_bingx = models.CharField(max_length=50,null=True)
    fpa = models.CharField(max_length=50,null=True)
    telephone = models.CharField(max_length=15,null=True)
    wallet = models.CharField(max_length=100,null=True)
    uplink = models.CharField(max_length=50,null=True)
    link = models.CharField(max_length=100)
    roles= models.CharField(max_length=50,default="user")
    registrado = models.BooleanField(default=False)
    aceptado= models.BooleanField(default=False)
    eliminado= models.BooleanField(default=False)
    broker_id= models.ForeignKey(Broker, on_delete=models.CASCADE)
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
        return self.fpa


class Cuenta(models.Model):
    id_monto = models.AutoField(primary_key=True, verbose_name='ID')
    fpa = models.CharField(max_length=50)
    monto_total = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    monto_a_pagar = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    spread_directo = models.DecimalField(max_digits=10, decimal_places=3, default=0.0) 
    spread_indirecto = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    monto_cpa = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    monto_bono_directo = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    monto_bono_indirecto = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    cpa = models.IntegerField(default=0)
    cpaIndirecto = models.IntegerField(default=0)
    level_bono_directo = models.IntegerField(default=0)
    level_bono_indirecto = models.IntegerField(default=0)
    retiros = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    have_bono = models.BooleanField(default=False)
    have_bono_indirecto = models.BooleanField(default=False)
    
    def __str__(self):
        return self.fpa


class PagoRealizado(models.Model):
    id_pagos = models.AutoField(primary_key=True, verbose_name='ID')
    fpa = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    monto_total = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    monto_cpa = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    monto_indirecto = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    monto_bono_indirecto = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    monto_bono_directo = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    
    def __str__(self):
        return self.fpa


class BonoAPagar(models.Model):
    id_bono = models.AutoField(primary_key=True, verbose_name='ID')
    fpa = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    monto_total = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    monto_bono_indirecto = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    monto_bono_directo = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    pagado = models.BooleanField(default=False)
    
    def __str__(self):
        return self.fpa