from django.urls import path
from apps.usuarios.controller.userController import users, postNewUser





app_name = "users"

urlpatterns = [
    path("prueba/", postNewUser, name="users"),
    # path("login/", login, name="users"),
    # path("users/<pk>", users, name="users_pk"),
]