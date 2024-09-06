
"""

La gestion de Usuario, crear modificar eliminar adminsitar va pasar al archivo userController.py
ubicado en apps/usuarios/controller

"""


from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from apps.api.skilling.models import Cuenta
from ....usuarios.models import Url, Usuario
from apps.api.skilling.models import Afiliado
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
import json 
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model



###########################################################################################################################
############################### Leer comentario de arriba #################################################################
###########################################################################################################################
                                                  ##
                                                ######
                                              ##########
                                            ##############
                                                #####
                                                #####
                                                #####
                                                #####
                                                #####
                                                




