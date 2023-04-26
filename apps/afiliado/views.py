from django.shortcuts import render
from .models import Afiliado,Cliente
from .forms import ClienteForm
from django.core.exceptions import ObjectDoesNotExist
import os
from django.conf import settings
from django.urls import reverse_lazy
from django.http import JsonResponse,HttpResponse
import telegram
from django.views.decorators.csrf import csrf_exempt
import logging
import asyncio

chat_id='@pruebapas'
token='6154942852:AAGfHB6dNhTOxc0gwg-Qnop4LnnMVf9jr8c'

def afiliado(request, idAfiliado):
    afiliado = False
    try:
        afiliado = Afiliado.objects.get(idAfiliado=idAfiliado)
        form = ClienteForm()
        context = {'afiliado': afiliado, 'idAfiliado': idAfiliado, 'form': form}
        return render(request, 'afiliado.html', context)
    except ObjectDoesNotExist:
        afiliado = False
        context = {'errorIdNoExiste':'El Socio Existe, por favor comuniquese con liveCommunity para mas informacion'}
        return render(request, 'error.html',context)

# Envio de mensaje a telegram
logger = logging.getLogger(__name__)


async def enviar_mensaje(msj,id,token):

    bot = telegram.Bot(token=token) # Reemplaza 'TU_TOKEN_DE_TELEGRAM' con tu token de Telegram
   
    await bot.send_message(chat_id=id, text=msj)


# MessageString = 'hola'
# print(MessageString)
# asyncio.run(enviar_mensaje(MessageString, chat_id, token))
    

def clienteform(request):
    if request.method == 'POST':
        
        # Obtener los demás datos del formulario
        nombre = request.POST.get('nombre').strip()
        apellido = request.POST.get('apellido').strip()
        correo = request.POST.get('correo').strip()
        telefono = request.POST.get('telefono').strip()
        idAfiliado = request.POST.get('idAfiliado').strip()
        userTelegram = request.POST.get('userTelegram').strip()
        idCliente = request.POST.get('idcliente').strip()
        
        # Crear un objeto de modelo con los datos del formulario, incluyendo la ruta del archivo
        cliente = Cliente(
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            telefono=telefono,
            idAfiliado=idAfiliado,
            userTelegram=userTelegram,
            idCliente=idCliente
        )
        cliente.save()  # Guardar el objeto en la base de datos
        mensaje = f"Nombre: {nombre}\nApellido: {apellido}\nUser Telegram: {userTelegram}\nEmail: {correo}\nTeléfono: {telefono}\nID Afiliado: {idAfiliado}\nID Cliente: {idCliente}"

        asyncio.run(enviar_mensaje(mensaje,chat_id,token))
        
    return render(request, 'linkGrupos.html')






    

