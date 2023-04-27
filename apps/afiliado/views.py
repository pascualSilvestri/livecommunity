from django.shortcuts import render
from .models import Afiliado,Cliente
from .forms import ClienteForm
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.urls import reverse_lazy
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from livecommunity.settings.base import TELEGRAM_BOT_TOKEN,CHAT_ID_BOT
import telegram
import os
import logging
import asyncio

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

#Envio de mensaje a hacia telegram
async def enviar_mensaje(msj,id,token):

    bot = telegram.Bot(token=token) # Reemplaza 'TU_TOKEN_DE_TELEGRAM' con tu token de Telegram
   
    await bot.send_message(chat_id=id, text=msj)


# MessageString = 'hola'
# print(MessageString)
# asyncio.run(enviar_mensaje(MessageString, chat_id, token))
    
#Verifica si el id ingresado no se encuentra en base de datos
def existe(clientes,idCliente):
    for client in clientes:
        if client.idCliente == idCliente:
            return True
    
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
        
        if not existe(clientes,idCliente):# si no existe el cliente ne base de datos, se guarda 
            cliente.save()  # Guardar el objeto en la base de datos
        
        #Mensaje formateado apra telegram
        mensaje = f"Nombre: {nombre}\nApellido: {apellido}\nUser Telegram: {userTelegram}\nEmail: {correo}\nTeléfono: {telefono}\nID Afiliado: {idAfiliado}\nID Cliente: {idCliente}"

        #Envio de mensaje a Telegram
        asyncio.run(enviar_mensaje(mensaje,chat_id,token))
        
    return render(request, 'linkGrupos.html')

#Enviar todos los idClientes en formato Json a una url y tomarla en JS 
def verificarNuevoCliente(request):
    idCliente = Cliente.objects.all()
    
    data = []
    
    for i in idCliente:
        data.append(i.idCliente)
    
    return JsonResponse({'data':data})
 
# def verificarNuevoCliente(request):
#     if request.method == "POST":
#         idCliente=request.POST.get('idNuevoCliente')

#         print(idCliente)

#         return HttpResponse("Respuesta de la vista")
