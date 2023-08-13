from django.urls import path
from . import views
from .controller.users import postNewUser,users,getUser,usuarioValido,eliminarUser,getUserById,updateUserById,updatePerfilUser,usersEliminados,usersPendientes,updatePassword,montosGet
from .controller.registros import verificar
from .controller.ganancias import gananciaGetAll,gananciasTotales,gananciasTotalUser,getRGananciasById,filtarGananciasCpa,filtradoGananciasRevshare,filtradoGananciasRevshareById,filtarGananciasCpaById,filterGananciasFecha,filter_ganancia_to_date_by_id
from .controller.files import upload_fpa,upload_registros,upload_cpa,limpiar_ganacias


app_name = 'api'


urlpatterns = [
      #Todos los registros de todos para Admin
      #return array de Registros
      path('verificar/',verificar,name='verificar'),
      #############################################################################################
      ########################             Ganancias                ###############################
      #############################################################################################
      #Todos los ganancias de todos para Admin
      #return array de Ganancias
      path('ganancias/', gananciaGetAll, name = 'ganancias'),
      #ganancias por usuario
      path('ganancias/<pk>/', getRGananciasById, name = 'gananciasById'),
      #total de ganancias Admin
      path('gananciastotal/', gananciasTotales, name = 'gananciasById'),
      #Suma de ganancias por usuario
      path('gananciatotaluser/<pk>/', gananciasTotalUser, name = 'ganaciaTotalUser'),
      #Filtrado por fecha ganancias
      path('filtrargananciasfecha/<desde>/<hasta>/', filterGananciasFecha, name = 'gananciasFiltradoFecha'),
      #Filtrado por CPA
      path('filtrarganaciascpa/', filtarGananciasCpa, name = 'filtradoCpa'),
      #Filtrado por CPA y id del usuario
      path('filtrarganaciascpa/<pk>', filtarGananciasCpaById, name = 'filtradoCpaById'),
      #Filtrado por Revshare
      path('filtrarganaciasrevshare/', filtradoGananciasRevshare, name = 'filtradoRevshare'),
      #Filtrado por Revshare y Id de usuario
      path('filtrarganaciasrevshare/<pk>/', filtradoGananciasRevshareById, name = 'filtradoRevshareById'),
      #############################################################################################
      ########################             Users                   ###############################
      #############################################################################################
      #registrar nuevo usuario en el backend
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
      path('usereliminados/', usersEliminados, name = 'userEliminados'),
      #retorna los usuario pendientes
      path('userpendientes/', usersPendientes, name = 'userPendientes'),
      #cambio de password
      path('updatepassword/<pk>/', updatePassword, name = 'updatePassword'),
      #############################################################################################
      ########################             Montos y Calculos        ###############################
      #############################################################################################
      path('montos/<pk>/', montosGet, name = 'montos'),
      #filtrar gancincias por  fecha y id Genera el monto a pagar de una fecha indicada
      path('montosbydate/<pk>/<desde>/<hasta>/', filter_ganancia_to_date_by_id, name = 'montosByDate'),
      #############################################################################################
      ########################             Archivos                 ###############################
      #############################################################################################
      path('archivofpa',upload_fpa,name = 'archivoFpa'),
      path('archivoregistros',upload_registros,name = 'archivoRegistros'),
      path('archivocpa',upload_cpa,name='archivoCpa'),
      path('archivoganancias',limpiar_ganacias,name='archivoGanancias'),
      
]     