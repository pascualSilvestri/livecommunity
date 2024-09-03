from django.contrib import admin
from .models import Usuario, Url, Referido, Rol, Servicio
# Register your models here.
admin.site.register(Usuario)
admin.site.register(Url)
admin.site.register(Referido)
admin.site.register(Rol)
admin.site.register(Servicio)

