from django.http import JsonResponse
from django.shortcuts import render
from livecommunity import settings
import telegram

from apps.api.skilling.forms import ClienteForm
from apps.api.skilling.models import  Relation_fpa_client
from ...usuarios.models import Rol, Servicio, Url, Usuario, UsuarioRol, UsuarioServicio
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.db import transaction
from apps.usuarios.models import Usuario
import json 
from livecommunity.settings import TELEGRAM_BOT_TOKEN,CHAT_ID_BOT
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail



chat_id = CHAT_ID_BOT
token = TELEGRAM_BOT_TOKEN


#Obtener afiliado por id y enviarlo a la vista afiliado.html
def afiliado(request, idAfiliado):
    afiliado = False
    try:
        afiliado = Usuario.objects.get(fpa=idAfiliado)
        urls = Url.objects.all()
        url = f'{urls[1].url}{idAfiliado}'
        
        
        form = ClienteForm()
        context = {'afiliado': afiliado, 'idAfiliado': idAfiliado, 'form': form, 'url': url}
        return render(request, 'afiliado.html', context)
    except ObjectDoesNotExist:
        afiliado = False
        context = {'errorIdNoExiste':'El Socio Existe, por favor comuniquese con liveCommunity para mas informacion'}
        return render(request, 'error.html',context)


