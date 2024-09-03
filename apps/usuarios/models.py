from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    # Campos adicionales personalizados
    fpa = models.CharField(max_length=50, null=True)
    idCliente = models.CharField(max_length=50, null=True)
    uplink = models.CharField(max_length=50, null=True, blank=True)
    telephone = models.CharField(max_length=15, null=True, blank=True)
    wallet = models.CharField(max_length=100, null=True, blank=True)
    userTelegram = models.CharField(max_length=200, default="none", null=True, blank=True)
    link = models.CharField(max_length=100, null=True, blank=True)
    registrado = models.BooleanField(default=False)
    aceptado = models.BooleanField(default=False)
    fondeado = models.BooleanField(default=False)
    eliminado = models.BooleanField(default=False)

    # Relaciones con otros usuarios (downLeft y downRight) inicializadas como null
    downLeft = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='down_left_user')
    downRight = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='down_right_user')

    # Relación muchos a muchos con Roles y Servicios
    roles_asignados = models.ManyToManyField('Rol', related_name='usuarios')
    servicios_asignados = models.ManyToManyField('Servicio', related_name='usuarios')

    def __str__(self):
        return self.username


class Url(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    url = models.URLField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='urls')

    def __str__(self):
        return self.name


class Referido(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='referidos')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Referido de {self.usuario.username} en {self.date}"


class Rol(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Servicio(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
