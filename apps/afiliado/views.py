from django.shortcuts import render
from .models import Afiliado,Cliente
from .forms import ClienteForm
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.urls import reverse_lazy
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from livecommunity.settings import TELEGRAM_BOT_TOKEN,CHAT_ID_BOT
import telegram
import os
import logging
import asyncio
from asgiref.sync import sync_to_async


chat_id = CHAT_ID_BOT
token = TELEGRAM_BOT_TOKEN


#Obtener afiliado por id y enviarlo a la vista afiliado.html
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



# MessageString = 'hola'
# print(MessageString)
# asyncio.run(enviar_mensaje(MessageString, chat_id, token))
    
#Verifica si el id ingresado no se encuentra en base de datos
def existe(clientes,idCliente):
    for client in clientes:
        if client.idCliente == idCliente:
            return True
        
#Envio de mensaje a hacia telegram
def enviar_mensaje_sync(msj, id, token):
    bot = telegram.Bot(token=token)
    bot.send_message(chat_id=id, text=msj)

#Obtiene los datos del form del front y los guarda en base de datos
#Tambien lo envia a telegram
#
def clienteform(request):
    clientes = Cliente.objects.all()
    
    
    if request.method == 'POST':
        
        # Obtener los demás datos del formulario
        nombre = request.POST.get('nombre').strip()
        apellido = request.POST.get('apellido').strip()
        correo = request.POST.get('correo').strip()
        telefono = request.POST.get('telefono').strip()
        idAfiliado2 = request.POST.get('idAfiliado').strip()
        userTelegram = request.POST.get('userTelegram').strip()
        idCliente = request.POST.get('idcliente').strip()
        
        afiliado2 = Afiliado.objects.get(idAfiliado = idAfiliado2).referenciaAfiliado.__str__()
    
        # Crear un objeto de modelo con los datos del formulario, incluyendo la ruta del archivo
        cliente = Cliente(
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            telefono=telefono,
            idAfiliado=idAfiliado2,
            userTelegram=userTelegram,
            idCliente=idCliente
        )
        
        if not existe(clientes,idCliente):# si no existe el cliente ne base de datos, se guarda 
            cliente.save()  # Guardar el objeto en la base de datos
        
        #Mensaje formateado apra telegram
        mensaje = f"Nombre: {nombre}\nApellido: {apellido}\nUser Telegram: {userTelegram}\nEmail: {correo}\nTeléfono: {telefono}\nID Socio1: {idAfiliado2}\nID Socio2: {afiliado2}\nID Cliente: {idCliente}"
        #Envio de mensaje a Telegram

        #
        # Local
        #        
        # asyncio.run(enviar_mensaje(mensaje,chat_id,token))
        
        #
        # Produccion
        #
        # loop = asyncio.get_event_loop()
        try:
            enviar_mensaje_sync(mensaje, chat_id, token)
        except Exception as e:
            return render(request, 'linkGrupos.html')

    return render(request, 'linkGrupos.html')


#################################################
# def verificarNuevoCliente(request):
#     idCliente = Verificar.objects.all()
    
#     data = []
    
#     for i in idCliente:
#         data.append(i.id)
    
#     return JsonResponse({'data':data})
##################################################
 
