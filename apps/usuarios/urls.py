from django.urls import path
from apps.usuarios.controller.userController import deleteUser, eliminarUser, getUserById, postNewAfiliado, postNewUser, login, updatePassword, updatePerfilUser, updateUserById, users, users_eliminados, users_pendientes, usuarioValido


app_name = "users"

urlpatterns = [
    path("register/", postNewUser, name="users"),
    path("login/", login, name="userEmail"),
    path("newafiliado/", postNewAfiliado, name="NewAfiliado"),
    path("users/", users, name="users"),
    path("existeuseremail/<email>/<password>", usuarioValido, name="existeUserEmail"),
    ################## Elimina un usuario logicamente, no de la base de datos ###########################################################
    path("eliminaruser/<pk>", eliminarUser, name="eliminarUsuario"),  # Revisar este endpoint por que no elimina usuario
    path("userid/<pk>/", getUserById, name="userId"),
    path("updateuser/<pk>/", updateUserById, name="updateUser"),
    path("updateperfiluser/<pk>/", updatePerfilUser, name="updatePerfilUser"),
    path("usereliminados/", users_eliminados, name="userEliminados"),
    path("userpendientes/", users_pendientes, name="userPendientes"),
    path("updatepassword/<pk>/", updatePassword, name="updatePassword"),
    path("deleteuser/<pk>/", deleteUser, name="deleteUser"),
]
