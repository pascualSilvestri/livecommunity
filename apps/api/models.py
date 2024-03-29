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