from django.contrib import admin
from .models import Usuario,BonoCpa,BonoCpaIndirecto,Spread,Cuenta
# Register your models here.
admin.site.register(Usuario)
admin.site.register(BonoCpa)
admin.site.register(BonoCpaIndirecto)
admin.site.register(Spread)
admin.site.register(Cuenta)