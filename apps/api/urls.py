from django.urls import path
from .skilling_servicios.users import postNewAfiliado,postNewUser,users,getUser,usuarioValido,eliminarUser,getUserById,updateUserById,updatePerfilUser,users_eliminados,users_pendientes,updatePassword,deleteUser
from .skilling_servicios.registros import verificar,registrosGetAll,getRegistroById,filter_registros_fecha_by_id
from .skilling_servicios.ganancias import ganancia_get_all,filtrar_ganancias_by_revshare_By_Id,ganancias_total_con_porcentaje,retiros_totales,ganancias_total_user,ganancias_total,ganancia_by_id,filtarGananciasCpa,filtradoGananciasRevshare,filtarGananciasCpaById,filterGananciasFecha,filter_ganancia_to_date_by_id,ganancias_cpa,ganancias_cpa_by_id,ganancias_all_for_id,ganancia_a_pagar,filterGananciasFechaById
from .skilling_servicios.cuenta import montosGet
from .skilling_servicios.files import upload_fpa,upload_registros,upload_cpa,upload_ganancias
from .skilling_servicios.bonos import reseteo_bonos,get_bono_cpa,put_bono_cpa,get_spread,get_bono_cpa_indirecto,put_bono_cpa_indirecto,put_spread

app_name = 'api'

urlpatterns = [
      #Todos los registros de todos para Admin
      #############################################################################################
      ########################             Registros                ###############################
      #############################################################################################
      #return array de Registros
      path('verificar/',verificar,name='verificar'),
      path('registros/',registrosGetAll,name='registros'),
      path('registrosbyid/<pk>/',getRegistroById,name='registrosById'),
      path('filtrarregistrosfecha/<pk>/<desde>/<hasta>/', filter_registros_fecha_by_id, name = 'registrosFiltradoFecha'),
      #############################################################################################
      ########################             Ganancias                ###############################
      #############################################################################################
      #Todos los ganancias de todos para Admin
      #return array de Ganancias
      path('ganancias/', ganancia_get_all, name = 'ganancias'),
      #ganancias por usuario
      path('ganancias/<pk>/', ganancia_by_id, name = 'gananciasById'),
      #total de ganancias Admin
      path('gananciatotal/', ganancias_total, name = 'ganaciaTotal'),
      path('gananciatotalconporcentaje/', ganancias_total_con_porcentaje, name = 'ganaciaTotal'),
      path('retiros/', retiros_totales, name = 'retiros'),
      #Suma de ganancias por usuario
      path('gananciatotaluser/<pk>/', ganancias_total_user, name = 'ganaciaTotalUser'),
      #Filtrado por fecha ganancias
      path('filtrargananciasfecha/<desde>/<hasta>/', filterGananciasFecha, name = 'gananciasFiltradoFecha'),
      path('filtrargananciasfechaById/<pk>/<desde>/<hasta>/', filterGananciasFechaById, name = 'gananciasFiltradoFecha'),
      #Filtrado por CPA
      path('filtrarganaciascpa/', filtarGananciasCpa, name = 'filtradoCpa'),
      #Filtrado por CPA y id del usuario
      path('filtrarganaciascpa/<pk>', filtarGananciasCpaById, name = 'filtradoCpaById'),
      #Filtrado por Revshare
      path('filtrarganaciasrevshare/', filtradoGananciasRevshare, name = 'filtradoRevshare'),
      #Filtrado por Revshare y Id de usuario
      path('filtrarganaciasrevshare/<pk>/', filtrar_ganancias_by_revshare_By_Id, name = 'filtradoRevshareById'),
      path('cpas/',ganancias_cpa,name='cpa'),
      path('cpas/<pk>/',ganancias_cpa_by_id,name='cpa'),
      path('gananciasallforid/<desde>/<hasta>/',ganancias_all_for_id,name='gananciasAllForId'),
      path('pagando/',ganancia_a_pagar, name ='pagando'),
      #############################################################################################
      ########################             Users                   ###############################
      #############################################################################################
      #registrar nuevo usuario en el backend
      path('newafiliado/', postNewAfiliado, name = 'NewAfiliado'),
      path('newuser/', postNewUser, name = 'NewUser'),
      #Si el correo y la contraseña existen en base de datos
      #return True o False
      path('existeuseremail/<email>/<password>', usuarioValido, name = 'existeUserEmail'),
      #usuario por email 
      #return todos los Usuarios
      path('users/', users, name = 'users'),
      #usuario por email
      #return un usuario del email que recibe
      path('user/<email>/', getUser, name = 'userEmail'),
      #user por el id del usuario
      path('userid/<pk>/', getUserById, name = 'userId'),
      #Elimina usuario de la vista no de la base de datos
      path('eliminaruser/<pk>',eliminarUser, name='eliminarUsuario' ),
      #Editar usuario
      path('updateuser/<pk>/', updateUserById, name = 'updateUser'),
      #modifica en perfil de usuario
      path('updateperfiluser/<pk>/', updatePerfilUser, name = 'updatePerfilUser'),
      #retorna los usuario eliminados
      path('usereliminados/', users_eliminados, name = 'userEliminados'),
      #retorna los usuario pendientes
      path('userpendientes/', users_pendientes, name = 'userPendientes'),
      #cambio de password
      path('updatepassword/<pk>/', updatePassword, name = 'updatePassword'),
      #eliminar usuario
      path('deleteuser/<pk>/', deleteUser, name = 'deleteUser'),
      #############################################################################################
      ########################             Montos y Calculos        ###############################
      #############################################################################################
      path('montos/<pk>/', montosGet, name = 'montos'),
      #filtrar gancincias por  fecha y id Genera el monto a pagar de una fecha indicada
      path('montosbydate/<pk>/<desde>/<hasta>/', filter_ganancia_to_date_by_id, name = 'montosByDate'),
      #############################################################################################
      ########################             Archivos                 ###############################
      #############################################################################################
      path('archivofpa/',upload_fpa,name = 'archivoFpa'),
      path('archivoregistros/',upload_registros,name = 'archivoRegistros'),
      path('archivocpa/',upload_cpa,name='archivoCpa'),
      path('archivoganancias/',upload_ganancias,name='archivoGanancias'),
      #############################################################################################
      ########################             Bonos                    ###############################
      #############################################################################################
      path('resetBono',reseteo_bonos , name='reset_bonos'),
      path('getbonocpa',get_bono_cpa , name='getbonocpa'),
      path('getspread',get_spread , name='getSpread'),
      path('getbonocpaindirecto',get_bono_cpa_indirecto , name='getbonocpaindirecto'),
      path('putbonocpa',put_bono_cpa , name='putbonocpa'),
      path('putbonocpaindirecto',put_bono_cpa_indirecto , name='putbonocpaindirecto'),
      path('putspread',put_spread , name='putSpread'),
      
]     