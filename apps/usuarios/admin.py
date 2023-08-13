from django.contrib import admin
from .models import Usuario,BonoCpa,BonoCpaIndirecto,Spread
# Register your models here.
admin.site.register(Usuario)
admin.site.register(BonoCpa)
admin.site.register(BonoCpaIndirecto)
admin.site.register(Spread)