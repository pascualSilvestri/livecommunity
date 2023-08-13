from django.contrib import admin

from .views import ArchivoAdmin
from .models import Verificar, Archivo


# admin.site.register(Verificar)
admin.site.register(Archivo,ArchivoAdmin)