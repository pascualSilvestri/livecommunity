from django.urls import path
from . import views
from .controller.registros import (
    proxy_request,
    filter_registros_fecha_by_id,
)
from .controller.ganancias import (
    get_historial_pagos_all,
    get_historial_pagos_by_fpa,
    obtener_ganancias_cpa_spread_bonos,
    obtener_ganancias_cpa_spread_bonos_todos,
    obtener_ganancias_cpa_spread_bonos_to_payment,
    post_registros_ganancias_pagadas
    
)
# from .controller.cuenta import montosGet
from .controller.files import upload_ganancias
from .controller.bonos import (
    get_bono_cpa,
    put_bono_cpa,
    get_spread,
    get_bono_cpa_indirecto,
    put_bono_cpa_indirecto,
    put_spread,
    create_allbonos,
)

app_name = "skilling"



urlpatterns = [

    ################## Procesar archivos ganancias ######################################################################################
    path("archivoganancias/", upload_ganancias, name="archivoGanancias"),
    ################## Resetear bonos ###################################################################################################
    ################## Filtrado de todos los registros de registro por fecha y id #######################################################
    path(
        "filtrarregistrosfecha/<pk>/<desde>/<hasta>/",
        filter_registros_fecha_by_id,
        name="registrosFiltradoFecha",
    ),
    

    ################## Obtiene el valor de las variables del bono de cpa indirecto ######################################################
    path("getbonocpaindirecto", get_bono_cpa_indirecto, name="getbonocpaindirecto"),
    ################## Modifica el valor de las variables del bono de cpa indirecto #####################################################
    path("putbonocpaindirecto", put_bono_cpa_indirecto, name="putbonocpaindirecto"),
    ################## Obtiene el valor de las variables del bono de cpa directo ########################################################
    path("getbonocpa", get_bono_cpa, name="getbonocpa"),
    ################## Modifica el valor de las variables del bono de cpa directo #######################################################
    path("putbonocpa", put_bono_cpa, name="putbonocpa"),
    ################## Obtiene el valor de las variables Spread  ########################################################################
    path("getspread", get_spread, name="getSpread"),
    ################## Modifica el valor de las variables Spread  #######################################################################
    path("putspread", put_spread, name="putSpread"),
    ################## Crea el valor de las variables de los bonos en base de datos #####################################################
    path("createAllbonos", create_allbonos, name="createAllbonos"),
    ################## Obtiene todos los montos de todos los registros y ganancias a pagar ##############################################
    ################## Elimina un usuario de la base de datos ###########################################################################
    
    path("proxy/<pk>/", proxy_request, name="proxy"),
    path("ganancias-cpa-bonos-by-fpa/<pk>/<desde>/<hasta>/", obtener_ganancias_cpa_spread_bonos, name="gananciasCpaBonosByFpa"),
    path("ganancias-cpa-bonos-all-users/<desde>/<hasta>/", obtener_ganancias_cpa_spread_bonos_todos, name="gananciasCpaBonosAllUsers"),
    path("ganancia-cpa-bonos-all-to-payment/<desde>/<hasta>/", obtener_ganancias_cpa_spread_bonos_to_payment, name="gananciaCpaBonosByAllToPayment"),
    path("post-registros-ganancia-pagadas/", post_registros_ganancias_pagadas, name="postRegistrosGanancia"),
    path("get-historial-pagos-all/", get_historial_pagos_all, name="getHistorialPagosAll"),
    path("get-historial-pagos-by-fpa/<fpa>/", get_historial_pagos_by_fpa, name="getHistorialPagosByFpa"),

    
]
