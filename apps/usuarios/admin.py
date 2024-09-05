from django.contrib import admin
from .models import Usuario, Url, Referido, Rol, Servicio, UsuarioUrl, UsuarioRol, UsuarioServicio

class UsuarioRolInline(admin.TabularInline):
    model = UsuarioRol
    extra = 1
    
class UsuarioServicioInline(admin.TabularInline):
    model = UsuarioServicio
    extra = 1

class UrlInline(admin.TabularInline):
    model = UsuarioUrl
    extra = 1
    fields = ('url','usuario')  

class UsuarioAdmin(admin.ModelAdmin):
    inlines = [UsuarioRolInline,UsuarioServicioInline,UrlInline]

admin.site.register(Usuario, UsuarioAdmin)
# Register your models here.
# admin.site.register(Usuario)
admin.site.register(Url)
admin.site.register(Referido)
admin.site.register(Rol)
admin.site.register(Servicio)
admin.site.register(UsuarioUrl)
admin.site.register(UsuarioRol)
admin.site.register(UsuarioServicio)

