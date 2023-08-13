from django.http import JsonResponse
from django.shortcuts import render
from ..usuarios.models import Usuario
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
import json 



