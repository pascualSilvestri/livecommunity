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
        return self.fpa

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
    fecha_creacion= models.DateField(null=True)
    monto= models.FloatField()
    cpa= models.CharField(max_length=50)
    client= models.CharField(max_length=50)
    fpa= models.CharField(max_length=50)
    pagado= models.BooleanField(default=False)
    
    def __str__(self):
        return self.fpa


class Registros_ganancias(models.Model):
    client = models.CharField(max_length=100)
    fpa=    models.CharField(max_length=200,null=True)
    full_name = models.CharField(max_length=200)
    country = models.CharField(max_length=50)
    equity = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    partner_earning = models.DecimalField(max_digits=10, decimal_places=2)
    skilling_earning = models.DecimalField(max_digits=10, decimal_places=2)
    skilling_markup = models.DecimalField(max_digits=10, decimal_places=2)
    skilling_commission = models.DecimalField(max_digits=10, decimal_places=2)
    volumen = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_last_trade = models.DateField(null=True)
    fecha_first_trade = models.DateField(null=True)
    closed_trade_count = models.PositiveIntegerField()
    customer_pnl = models.DecimalField(max_digits=10, decimal_places=2)
    deposito_neto = models.DecimalField(max_digits=10, decimal_places=2)
    deposito = models.CharField(max_length=50)
    withdrawals = models.CharField(max_length=50)

    def __str__(self):
        return self.client
    