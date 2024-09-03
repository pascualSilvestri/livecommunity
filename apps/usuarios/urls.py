from django.urls import path
from apps.usuarios.controller.userController import users





app_name = "users"

urlpatterns = [
    path("prueba/", users, name="users"),
    # path("login/", login, name="users"),
    # path("users/<pk>", users, name="users_pk"),
]