from django.contrib import admin

# Register your models here.
from .models import Relation_fpa_client,Registro_archivo,Registros_cpa,Registros_ganancias,SpreadIndirecto
# Register your models here.
admin.site.register(Relation_fpa_client)
admin.site.register(Registro_archivo)
admin.site.register(Registros_cpa)
admin.site.register(Registros_ganancias)
admin.site.register(SpreadIndirecto)