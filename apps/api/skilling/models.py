from django.db import models

# Create your models here.

class Fpas(models.Model):
    id = models.AutoField(primary_key=True)
    fpa = models.CharField(max_length=50)
    fecha_creacion = models.DateField(null=True)
    fecha_verificacion = models.DateField(null=True)
    status = models.CharField(max_length=100, null=True)

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

class CpaIndirecto(models.Model):
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


class Spread_directo_pagado(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.CharField(max_length=100)
    symbol = models.CharField(max_length=100)
    deal_id = models.CharField(max_length=100)
    fpa = models.CharField(max_length=200, null=True)
    full_name = models.CharField(max_length=200)
    partner_earning = models.DecimalField(max_digits=10, decimal_places=2)
    monto_a_pagar = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_operacion = models.DateField(null=True)
    position = models.CharField(max_length=100)
    spreak_direct = models.FloatField(default=0)
    spreak_indirecto = models.FloatField(default=0)
    spreak_socio = models.FloatField(default=0)
    pagado = models.BooleanField(default=False)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_desde = models.DateField(null=True)
    fecha_hasta = models.DateField(null=True)
    fecha_pagado = models.DateField(auto_now_add=True)
    registros_ganancia_pagadas = models.ForeignKey('Registros_ganancia_pagadas', on_delete=models.CASCADE, related_name='spread_directo_pagado')

    def __str__(self):
        return self.client


class Spread_indirecto_pagado(models.Model):
    id = models.AutoField(primary_key=True)
    id_spread_indirecto = models.CharField(max_length=50)
    monto = models.FloatField()
    fpa_child = models.CharField(max_length=50)
    fpa = models.CharField(max_length=50)
    fecha_creacion = models.DateField(null=True)
    pagado = models.BooleanField(default=False)
    fecha_pagado = models.DateField(auto_now_add=True)
    fecha_desde = models.DateField(null=True)
    fecha_hasta = models.DateField(null=True)
    registros_ganancia_pagadas = models.ForeignKey('Registros_ganancia_pagadas', on_delete=models.CASCADE, related_name='spread_indirecto_pagado')

    def __str__(self):
        return self.fpa


class Cpa_directo_pagado(models.Model):
    id = models.AutoField(primary_key=True)
    commission_id = models.CharField(max_length=50)
    monto = models.FloatField()
    client = models.CharField(max_length=50)
    fpa = models.CharField(max_length=50)
    fecha_creacion = models.DateField(null=True)
    fecha_desde = models.DateField(null=True)
    fecha_hasta = models.DateField(null=True)
    tipo_comision = models.CharField(max_length=100)
    fecha_pagado = models.DateField(auto_now_add=True)
    registros_ganancia_pagadas = models.ForeignKey('Registros_ganancia_pagadas', on_delete=models.CASCADE, related_name='cpa_directo_pagado')

    def __str__(self):
        return self.client


class Cpa_indirecto_pagado(models.Model):
    id = models.AutoField(primary_key=True)
    commission_id = models.CharField(max_length=50)
    monto = models.FloatField()
    client = models.CharField(max_length=50)
    fpa_child = models.CharField(max_length=50)
    fpa = models.CharField(max_length=50)
    fecha_creacion = models.DateField(null=True)
    fecha_desde = models.DateField(null=True)
    fecha_hasta = models.DateField(null=True)
    tipo_comision = models.CharField(max_length=100)
    fecha_pagado = models.DateField(auto_now_add=True)
    registros_ganancia_pagadas = models.ForeignKey('Registros_ganancia_pagadas', on_delete=models.CASCADE, related_name='cpa_indirecto_pagado')

    def __str__(self):
        return self.fpa


class Bono_indirecto_pagado(models.Model):
    id = models.AutoField(primary_key=True)
    monto = models.FloatField()
    fpa = models.CharField(max_length=50)
    nivel = models.IntegerField()
    fecha_desde = models.DateField(null=True)
    fecha_hasta = models.DateField(null=True)
    fecha_pagado = models.DateField(auto_now_add=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    registros_ganancia_pagadas = models.ForeignKey('Registros_ganancia_pagadas', on_delete=models.CASCADE, related_name='bono_indirecto_pagado')

    def __str__(self):
        return self.fpa


class Bono_directo_pagado(models.Model):
    id = models.AutoField(primary_key=True)
    monto = models.FloatField()
    fpa = models.CharField(max_length=50)
    nivel = models.IntegerField()
    fecha_desde = models.DateField(null=True)
    fecha_hasta = models.DateField(null=True)
    fecha_pagado = models.DateField(auto_now_add=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    registros_ganancia_pagadas = models.ForeignKey('Registros_ganancia_pagadas', on_delete=models.CASCADE, related_name='bono_directo_pagado')

    def __str__(self):
        return self.fpa
    
class Registros_ganancia_pagadas(models.Model):
    id = models.AutoField(primary_key=True)
    fpa = models.CharField(max_length=50, null=True)
    fecha_desde = models.DateField(null=True)
    fecha_hasta = models.DateField(null=True)
    monto_total = models.FloatField()
    monto_spread_directo = models.FloatField()
    monto_spread_indirecto = models.FloatField()
    monto_cpa_directo = models.FloatField()
    monto_cpa_indirecto = models.FloatField()
    monto_bono_directo = models.FloatField()
    monto_bono_indirecto = models.FloatField()
    nivel_bono_directo = models.IntegerField()
    nivel_bono_indirecto = models.IntegerField()
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.fpa
    
    

################################### Modelo a eliminar ###################################

# class Relation_fpa_client(models.Model):
#     id = models.AutoField(primary_key=True)
#     fpa = models.CharField(max_length=50)
#     client = models.CharField(max_length=100,null=True)
#     full_name= models.CharField(max_length=200,null=True)
#     country= models.CharField(max_length=50,null=True)    
#     fecha_registro=models.DateField(null=True,auto_now_add=True)
#     fecha_creacion=models.DateField(null=True)
#     fecha_verificacion= models.DateField(null=True)
#     status = models.CharField(max_length=100,null=True)
    
#     def __str__(self):
#         return self.client