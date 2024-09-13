from django.urls import path
from . import views
from .controller.registros import (
    verificar,
    registrosGetAll,
    getRegistroById,
    filter_registros_fecha_by_id,
)
from .controller.ganancias import (
    ganancia_get_all,
    filtrar_ganancias_by_revshare_By_Id,
    ganancias_total_con_porcentaje,
    retiros_totales,
    ganancias_total_user,
    ganancias_total,
    ganancia_by_id,
    filtarGananciasCpa,
    filtradoGananciasRevshare,
    filtarGananciasCpaById,
    filterGananciasFecha,
    filter_ganancia_to_date_by_id,
    ganancias_cpa,
    ganancias_cpa_by_id,
    ganancias_all_for_id,
    ganancia_a_pagar,
    filterGananciasFechaById,
)
# from .controller.cuenta import montosGet
from .controller.files import upload_fpa, upload_registros, upload_cpa, upload_ganancias
from .controller.bonos import (
    reseteo_bonos,
    get_bono_cpa,
    put_bono_cpa,
    get_spread,
    get_bono_cpa_indirecto,
    put_bono_cpa_indirecto,
    put_spread,
    create_allbonos,
)

app_name = "skilling"

"""
urls.py

This file contains all the URLs of the skilling app.

The URLs are divided into the following sections:

* Login de usuario
* Registrar nuevo Afiliado
* Obtener usuario por el id
* Procesar archivos fpa
* Procesar archivos registro
* Procesar archivos cpa
* Procesar archivos ganancias
* Resetear bonos
* Cambio de contraseña basico por el perfil del usuario
* Crear usuario Socio
* Obtener todos los registros de ganancias
* Obtener todos los registros de ganancias  por id
* Filtrado de todos los registros de ganancias por id
* Filtrado de todos los registros de ganancias por fecha y id
* Filtrado de todos los registros de ganancias por id y fecha
* Elimina un usuario logicamente, no de la base de datos
* Actualiza el perfil del usuario
* Obtiene todos los usuarios eliminados
* Obtiene todos los usuarios pendientes
* Procesa el pago de ganancias
* Obtiene el valor de las variables del bono de cpa indirecto
* Modifica el valor de las variables del bono de cpa indirecto
* Obtiene el valor de las variables del bono de cpa directo
* Modifica el valor de las variables del bono de cpa directo
* Obtiene el valor de las variables Spread
* Modifica el valor de las variables Spread
* Crea el valor de las variables de los bonos en base de datos
* Obtiene todos los registros de registros por id
* Obtiene todos los registros de registros
* Obtiene todos los montos de todos los registros y ganancias a pagar
* Obtiene todos los montos de todos los registros y ganancia a pagar por fecha
* Verifica si el cliente ya fondeo su cuenta y existe si idCliente en la DB para la pagina de registro
* Elimina un usuario de la base de datos

"""

urlpatterns = [

    ################## Procesar archivos fpa ############################################################################################
    path("archivofpa/", upload_fpa, name="archivoFpa"),
    ################## Procesar archivos registro #######################################################################################
    path("archivoregistros/", upload_registros, name="archivoRegistros"),
    ################## Procesar archivos cpa ############################################################################################
    path("archivocpa/", upload_cpa, name="archivoCpa"),
    ################## Procesar archivos ganancias ######################################################################################
    path("archivoganancias/", upload_ganancias, name="archivoGanancias"),
    ################## Resetear bonos ###################################################################################################
    path( "resetBono", reseteo_bonos, name="reset_bonos"),  # Este endpoint va ser eliminaod cuando se elimine el boton de resetar bonos
    ################## Cambio de contraseña basico por el perfil del usuario ############################################################
    
    ################## Obtener todos los registros de ganancias #########################################################################
    path("ganancias/", ganancia_get_all, name="ganancias"),
    ################## Obtener todos los registros de ganancias  por id #################################################################
    path("ganancias/<pk>/", ganancia_by_id, name="gananciasById"),
    ################## Filtrado de todos los registros de ganancias por id ##############################################################
    path("filtrarganaciascpa/<pk>", filtarGananciasCpaById, name="filtradoCpaById"),
    ################## Filtrado de todos los registros de reveshare por id ##############################################################
    path(
        "filtrarganaciasrevshare/<pk>/",
        filtrar_ganancias_by_revshare_By_Id,
        name="filtradoRevshareById",
    ),
    ################## Filtrado de todos los registros de ganancias por fecha y id ######################################################
    path(
        "gananciasallforid/<desde>/<hasta>/",
        ganancias_all_for_id,
        name="gananciasAllForId",
    ),
    ################## Modificar usuario por id #########################################################################################
    
    ################## Filtrado de todos los registros de ganancias por id y fecha ######################################################
    path(
        "filtrargananciasfechaById/<pk>/<desde>/<hasta>/",
        filterGananciasFechaById,
        name="gananciasFiltradoFecha",
    ),
    ################## Filtrado de todos los registros de ganancia por fecha ############################################################
    path(
        "filtrargananciasfecha/<desde>/<hasta>/",
        filterGananciasFecha,
        name="gananciasFiltradoFecha",
    ),
    ################## Filtrado de todos los registros de registro por fecha y id #######################################################
    path(
        "filtrarregistrosfecha/<pk>/<desde>/<hasta>/",
        filter_registros_fecha_by_id,
        name="registrosFiltradoFecha",
    ),
    
    ################## Actualiza el perfil del usuario ##################################################################################
    
    ################## Obtiene todos los usuarios eliminados ############################################################################
    
    ################## Obtiene todos los usuarios pendientes ############################################################################
    
    ################## Procesa el pago de ganancias #####################################################################################
    path("pagando/", ganancia_a_pagar, name="pagando"),
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
    ################## Obtiene todos los registros de registros por id ##################################################################
    path("registrosbyid/<pk>/", getRegistroById, name="registrosById"),
    ################## Obtiene todos los registros de registros #########################################################################
    path("registros/", registrosGetAll, name="registros"),
    ################## Obtiene todos los montos de todos los registros y ganancias a pagar ##############################################
    # path("montos/<pk>/", montosGet, name="montos"),
    ################## Obtiene todos los montos de todos los registros y ganancia a pagar por fecha #####################################
    path(
        "montosbydate/<pk>/<desde>/<hasta>/",
        filter_ganancia_to_date_by_id,
        name="montosByDate",
    ),
    ################## Verifica si el cliente ya fondeo su cuenta y existe si idCliente en la DB para la pagina de registro #############
    path("verificar/", verificar, name="verificar"),
    ################## Elimina un usuario de la base de datos ###########################################################################
    
    #####################################################################################################################################
    ########################3###### Area de los que no se estan usando y chequear ######################################
    #####################################################################################################################################
    path("filtrarganaciascpa/", filtarGananciasCpa, name="filtradoCpa"),
    path(
        "filtrarganaciasrevshare/", filtradoGananciasRevshare, name="filtradoRevshare"
    ),
    path("gananciatotal/", ganancias_total, name="ganaciaTotal"),
    path(
        "gananciatotalconporcentaje/",
        ganancias_total_con_porcentaje,
        name="ganaciaTotal",
    ),
    path("retiros/", retiros_totales, name="retiros"),
    path("gananciatotaluser/<pk>/", ganancias_total_user, name="ganaciaTotalUser"),
    path("cpas/", ganancias_cpa, name="cpa"),
    path("cpas/<pk>/", ganancias_cpa_by_id, name="cpa"),
    
    
]
