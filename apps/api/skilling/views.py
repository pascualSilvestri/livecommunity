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



@transaction.atomic
def clienteform(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.POST.get('first_name').strip()
        apellido = request.POST.get('last_name').strip()
        correo = request.POST.get('email').strip()
        telefono = request.POST.get('telephone').strip()
        fpa = request.POST.get('fpa').strip()
        userTelegram = request.POST.get('userTelegram').strip()
        idCliente = request.POST.get('idcliente').strip()
        
        # Buscar el FPA correspondiente
        registro = Relation_fpa_client.objects.filter(client=idCliente).first()
        fpa = registro.fpa if registro else ''
        
        # Buscar el upline
        afiliado = Usuario.objects.filter(fpa=fpa).first()
        upline = afiliado.up_line if afiliado else None

        # Generar una contraseña temporal
        temp_password = Usuario.objects.make_random_password()
        

        # Crear o actualizar Usuario
        usuario, created = Usuario.objects.update_or_create(
            email=correo,
            defaults={
                'username': correo,  # Usando el correo como nombre de usuario
                'password': make_password(temp_password),
                'first_name': nombre,
                'last_name': apellido,
                'fpa': None,
                'idCliente': idCliente,
                'telephone': telefono,
                'userTelegram': userTelegram,
                'up_line': fpa,
                'link': f"https://livecommunity.info/Afiliado/{fpa}" if fpa else None,
            }
        )
        rol = Rol.objects.get(id=3)
        servicio = Servicio.objects.get(id=1)
        if created:
            if not UsuarioRol.objects.filter(usuario=usuario, rol=rol).exists():
                UsuarioRol.objects.create(usuario=usuario, rol=rol)
         
        
            if not UsuarioServicio.objects.filter(usuario=usuario, servicio=servicio).exists():
                UsuarioServicio.objects.create(usuario=usuario, servicio=servicio)
                
            ########################### Enviar correo si se crea el usuario ###########################
            # enviar_correo(nombre,telefono,correo,idCliente,temp_password)
        
        if not created:
            if not UsuarioRol.objects.filter(usuario=usuario, rol=rol).exists():
                UsuarioRol.objects.create(usuario=usuario, rol=rol)
         
        
            if not UsuarioServicio.objects.filter(usuario=usuario, servicio=servicio).exists():
                UsuarioServicio.objects.create(usuario=usuario, servicio=servicio)
                
                
                
        # Mensaje formateado para telegram
        mensaje = f"Nombre: {nombre}\nApellido: {apellido}\nUser Telegram: {userTelegram}\nEmail: {correo}\nTeléfono: {telefono}\nID Socio1: {fpa}\nID Socio2: {upline}\nID Cliente: {idCliente}"
        
        try:
            enviar_mensaje_sync(mensaje, chat_id, token)
            
        except Exception as e:
            print(e.__str__())

    return render(request, 'linkGrupos.html')

# Función para enviar correo con contraseña temporal (implementar según tus necesidades)
def enviar_correo(nombre, telefono, correo, id_cliente, password_temporal):
    asunto = 'Bienvenido a LiveCommunity - Información de tu cuenta'
    mensaje = f"""
    Hola {nombre},

    ¡Bienvenido a LiveCommunity! Tu cuenta ha sido creada exitosamente.

    Aquí están los detalles de tu cuenta:
    
    Nombre: {nombre}
    Teléfono: {telefono}
    Correo electrónico: {correo}
    ID de Cliente: {id_cliente}
    
    Tu contraseña temporal es: {password_temporal}
    
    Por favor, ingresa a nuestra plataforma y cambia tu contraseña lo antes posible.

    Si tienes alguna pregunta o necesitas ayuda, no dudes en contactarnos.

    ¡Gracias por unirte a LiveCommunity!

    Saludos,
    El equipo de LiveCommunity
    """
    
    lista_destinatarios = [correo]  # Enviamos el correo al usuario
    correo_remitente = settings.EMAIL_HOST_USER

    try:
        send_mail(asunto, mensaje, correo_remitente, lista_destinatarios, fail_silently=False)
        print(f"Correo enviado exitosamente a {correo}")
        return True
    except Exception as e:
        print(f"Error al enviar el correo: {str(e)}")
        return False


