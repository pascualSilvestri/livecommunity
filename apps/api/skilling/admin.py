from django.contrib import admin
from .models import CPA, BonoAPagar, BonoCpa, BonoCpaIndirecto, Registros_ganancias, Spread,SpreadIndirecto,Cpa_a_pagar, Bono_directo_pagado, Bono_indirecto_pagado, Cpa_directo_pagado, Cpa_indirecto_pagado, CpaIndirecto, Spread_directo_pagado, Spread_indirecto_pagado,Registros_ganancia_pagadas, Fpas
# Register your models here.
admin.site.register(Registros_ganancias)
admin.site.register(SpreadIndirecto)
admin.site.register(Cpa_a_pagar)
admin.site.register(BonoCpa)
admin.site.register(BonoCpaIndirecto)
admin.site.register(Spread)
admin.site.register(BonoAPagar)
admin.site.register(CPA)
admin.site.register(Bono_directo_pagado)
admin.site.register(Bono_indirecto_pagado)
admin.site.register(Cpa_directo_pagado)
admin.site.register(Cpa_indirecto_pagado)
admin.site.register(CpaIndirecto)
admin.site.register(Spread_directo_pagado)
admin.site.register(Spread_indirecto_pagado)
admin.site.register(Registros_ganancia_pagadas)
admin.site.register(Fpas)

