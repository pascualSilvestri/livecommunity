from django.db import models
from django.contrib.auth.models import AbstractUser


class Rol(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name} ({self.id})'
    
class Servicio(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Url(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    url = models.URLField()
    
    def __str__(self):
        return self.name




class Usuario(AbstractUser):
    # Campos adicionales personalizados
    fpa = models.CharField(max_length=50, null=True)
    idCliente = models.CharField(max_length=50, null=True)
    up_line = models.CharField(max_length=50, null=True, blank=True)
    telephone = models.CharField(max_length=15, null=True, blank=True)
    wallet = models.CharField(max_length=100, null=True, blank=True)
    userTelegram = models.CharField(max_length=200, default="none", null=True, blank=True)
    userDiscord = models.CharField(max_length=200, default="none", null=True, blank=True)
    link = models.CharField(max_length=100, null=True, blank=True)
    registrado = models.BooleanField(default=False)
    aceptado = models.BooleanField(default=False)
    fondeado = models.BooleanField(default=False)
    eliminado = models.BooleanField(default=False)
    isSocio = models.BooleanField(default=False)
    url_video = models.URLField(default="https://www.youtube.com/watch?v=HgKjhFEguy")

    # Relaciones con otros usuarios (downLeft y downRight) inicializadas como null
    downLeft = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='down_left_user')
    downRight = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='down_right_user')

  # Relación muchos a muchos con una tabla intermedia personalizada
    roles_asignados = models.ManyToManyField(Rol, through='UsuarioRol', related_name='usuarios_con_roles')

    servicios_asignados = models.ManyToManyField(Servicio, through='UsuarioServicio', related_name='usuarios_con_servicios')
    

    def __str__(self):
        return self.username


class UsuarioRol(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='roles')
    rol = models.ForeignKey('Rol', on_delete=models.CASCADE, related_name='usuarios')
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rol.name} de {self.usuario.username}"


class UsuarioServicio(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='serviciosUsuario')
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='usuariosServico')
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.servicio.name} de {self.usuario.username}"



class Referido(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='referidos')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Referido de {self.usuario.username} en {self.date}"


class TokenPassword(models.Model):
    id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=100)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='token_password')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_expiracion = models.DateTimeField()

    def __str__(self):
        return self.token