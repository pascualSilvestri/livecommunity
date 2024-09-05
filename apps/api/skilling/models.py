from django.db import models

# Create your models here.

class Relation_fpa_client(models.Model):
    id = models.AutoField(primary_key=True)
    fpa = models.CharField(max_length=50)
    client = models.CharField(max_length=100)
    full_name= models.CharField(max_length=200)
    country= models.CharField(max_length=50)    
    fecha_registro=models.DateField(null=True)
    fecha_creacion=models.DateField(null=True)
    fecha_verificacion= models.DateField(null=True)
    status = models.CharField(max_length=100,null=True)
    
    def __str__(self):
        return self.client

class Registro_archivo(models.Model):
    id= models.AutoField(primary_key=True)
    client= models.CharField(max_length=50)
    fecha_registro= models.DateField(null=True)
    fpa= models.CharField(max_length=50,null=True)
    status= models.CharField(max_length=100,null=True)
    fecha_calif= models.DateField(null=True)
    country= models.CharField(max_length=30)
    posicion_cuenta= models.FloatField(default=0)
    volumen= models.FloatField(default=0)
    primer_deposito= models.FloatField(default=0)
    fecha_primer_deposito= models.DateField(null=True)
    neto_deposito= models.FloatField(default=0)
    numeros_depositos= models.FloatField(default=0)
    comision= models.FloatField(default=0)
    
    def __str__(self):
        return self.client


class Registros_cpa(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_creacion= models.DateField(null=True)
    monto_real= models.FloatField()
    monto= models.FloatField()
    cpa= models.CharField(max_length=50)
    client= models.CharField(max_length=50)
    fpa= models.CharField(max_length=50)
    pagado= models.BooleanField(default=False)
    
    def __str__(self):
        return self.fpa


class Registros_ganancias(models.Model):
    id= models.AutoField(primary_key=True)
    client = models.CharField(max_length=100)
    symbol=models.CharField(max_length=100)
    deal_id=models.CharField(max_length=100)
    fpa=models.CharField(max_length=200,null=True)
    full_name = models.CharField(max_length=200)
    partner_earning = models.DecimalField(max_digits=10, decimal_places=2)
    monto_a_pagar= models.DecimalField(max_digits=10, decimal_places=2)
    fecha_operacion = models.DateField(null=True)
    position=models.CharField(max_length=100)
    spreak_direct = models.FloatField(default=0)
    spreak_indirecto = models.FloatField(default=0)
    spreak_socio = models.FloatField(default=0)
    pagado = models.BooleanField(default=False)

    def __str__(self):
        return self.client


class Cpa_a_pagar(models.Model):
    id= models.AutoField(primary_key=True)
    monto= models.FloatField()
    client= models.CharField(max_length=50)
    fpa= models.CharField(max_length=50)
    fecha_creacion= models.DateField(auto_created=True)
    pagado = models.BooleanField(default=False)
    
    def __str__(self):
        return self.client



class SpreadIndirecto(models.Model):
    id= models.AutoField(primary_key=True)
    monto= models.FloatField()
    fpa_child= models.CharField(max_length=50)
    fpa= models.CharField(max_length=50)
    fecha_creacion= models.DateField(auto_created=True)
    pagado = models.BooleanField(default=False)
    
    def __str__(self):
        return self.fpa



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
    