from django.urls import path
from apps.usuarios.controller.passwordController import enviar_token_recuperacion
from apps.usuarios.controller.userController import deleteUser, eliminarUser, eliminarUserForever, getRoles, getServicios, getUserById, postNewAfiliado, postNewUser, login, postNewUsers, updatePassword, updatePerfilUser, updateUserById, users, users_eliminados, users_pendientes, usuarioValido
from .controller import passwordController

app_name = "users"

urlpatterns = [
    path("register/", postNewUser, name="user"),
    path("registers/", postNewUsers, name="users"),
    path("login/", login, name="userEmail"),
    path("newafiliado/", postNewAfiliado, name="NewAfiliado"),
    path("users/", users, name="users"),
    path("existeuseremail/<email>/<password>", usuarioValido, name="existeUserEmail"),
    ################## Elimina un usuario logicamente, no de la base de datos ###########################################################
    path("eliminaruser/<pk>/", eliminarUser, name="eliminarUsuario"),  # Revisar este endpoint por que no elimina usuario
    path("eliminaruserforever/<pk>/", eliminarUserForever, name="eliminarUsuarioForever"),
    path("userid/<pk>/", getUserById, name="userId"),
    path("updateuser/<pk>/", updateUserById, name="updateUser"),
    path("updateperfiluser/<pk>/", updatePerfilUser, name="updatePerfilUser"),
    path("usereliminados/", users_eliminados, name="userEliminados"),
    path("userpendientes/", users_pendientes, name="userPendientes"),
    path("updatepassword/<pk>/", updatePassword, name="updatePassword"),
    path("deleteuser/<pk>/", deleteUser, name="deleteUser"),
    path("roles/", getRoles, name="roles"),
    path("servicios/",getServicios,name="servicios"),
    path("enviar-token/", enviar_token_recuperacion, name="enviar_token_recuperacion"),
    path('validartoken/', passwordController.validar_token, name='validar_token'),
]
