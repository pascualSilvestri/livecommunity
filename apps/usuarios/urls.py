from django.urls import path
from apps.usuarios.controller.passwordController import enviar_token_recuperacion
from apps.usuarios.controller.userController import (
    addfpas,
    asociar_documento_con_idSkilling,
    deleteUser,
    eliminarUser,
    eliminarUserForever,
    getRoles,
    getServicios,
    getUserById,
    post_roles_servicios_user,
    postNewUser,
    login,
    postNewUsers,
    updatePassword,
    updatePerfilUser,
    updateUserById,
    users,
    usuarioValido,
    getFpasForUser,
    registrar_usuario,
)
from .controller import passwordController

app_name = "users"

urlpatterns = [
    path("clienteForm/<pk>/", registrar_usuario, name="clienteform"),
    path("register/", postNewUser, name="user"),
    path("registers/", postNewUsers, name="users"),
    path("login/", login, name="userEmail"),
    # path("newafiliado/", postNewAfiliado, name="NewAfiliado"),
    path("users/", users, name="users"),
    path("existeuseremail/<email>/<password>", usuarioValido, name="existeUserEmail"),
    ################## Elimina un usuario logicamente, no de la base de datos ###########################################################
    path(
        "eliminaruser/<pk>/", eliminarUser, name="eliminarUsuario"
    ),  # Revisar este endpoint por que no elimina usuario
    path(
        "eliminaruserforever/<pk>/", eliminarUserForever, name="eliminarUsuarioForever"
    ),
    path("userid/<pk>/", getUserById, name="userId"),
    path("updateuser/<pk>/", updateUserById, name="updateUser"),
    path("updateperfiluser/<pk>/", updatePerfilUser, name="updatePerfilUser"),
    path("updatepassword/<pk>/", updatePassword, name="updatePassword"),
    path("deleteuser/<pk>/", deleteUser, name="deleteUser"),
    path("roles/", getRoles, name="roles"),
    path("servicios/", getServicios, name="servicios"),
    path("enviar-token/", enviar_token_recuperacion, name="enviar_token_recuperacion"),
    path("validartoken/", passwordController.validar_token, name="validar_token"),
    path(
        "verificar-password-actual/",
        passwordController.verificar_password_actual,
        name="verificar_password_actual",
    ),
    path("get-fpas/<pk>/", getFpasForUser, name="getFpasForUser"),
    path("asociar-documento-idskilling/", asociar_documento_con_idSkilling, name="asociar_documento_con_idSkilling"),
    path("post-roles-servicios-user/", post_roles_servicios_user, name="post_roles_servicios_user"),
    path("addfpas/", addfpas, name="addfpas"),
]
