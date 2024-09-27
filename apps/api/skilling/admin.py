from django.contrib import admin
from .models import CPA, BonoAPagar, BonoCpa, BonoCpaIndirecto, Cuenta, Relation_fpa_client,Registro_archivo,Registros_cpa,Registros_ganancias, Spread,SpreadIndirecto,Cpa_a_pagar, PagoRealizado
# Register your models here.
admin.site.register(Relation_fpa_client)
admin.site.register(Registro_archivo)
admin.site.register(Registros_cpa)
admin.site.register(Registros_ganancias)
admin.site.register(SpreadIndirecto)
admin.site.register(Cpa_a_pagar)
admin.site.register(BonoCpa)
admin.site.register(BonoCpaIndirecto)
admin.site.register(Spread)
admin.site.register(Cuenta)
admin.site.register(BonoAPagar)
admin.site.register(CPA)
admin.site.register(PagoRealizado)

