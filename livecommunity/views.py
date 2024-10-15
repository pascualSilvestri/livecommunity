from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import json

from apps.usuarios.models import Url, Usuario



def home(request):

    url_video_insercion =convertir_url_youtube ("https://www.youtube.com/embed/k88AjonUhMw")
    url_register = f'/registro/LA500S'
    context = {
        "afiliado": None,
        "url_video": url_video_insercion,
        "url_register": url_register,
    }
    return render(request, "index.html",context)


# PRIMER SPRIG
def broker_skilling(request):
    url_register = "/registro/LM500S"
    context ={
        "afiliado": None,
        "url_register": url_register
    }
    return render(request,'broker.html',context)


def presenciales(request):
    url_register = "/registro/LM500S"
    context ={
        "afiliado": None,
        "url_register": url_register
    }
    return render(request, "presenciales.html",context)


def servicios(request):
    url_register = "/registro/LM500S"
    context ={
        "afiliado": None,
        "url_register": url_register
    }
    return render(request, "servicios.html",context)


def home_pk(request, pk):
    try:
        afiliado = Usuario.objects.get(fpa=pk)
        url = f'/registro/'
        if afiliado:
        # url_video_insercion = "https://www.youtube.com/watch?v=HgKjhFEguyU" if afiliado.url_video==0 or afiliado.url_video==''  else  convertir_url_youtube(afiliado.url_video) 
            url_video_insercion =convertir_url_youtube ("https://www.youtube.com/embed/k88AjonUhMw")
            url_register = f'{url}{pk}'
            context = {
            "afiliado": afiliado,
            "id":afiliado.fpa,
            "url_video": url_video_insercion,
            "url_register": url_register,
            
            }
        else:
            url_video_insercion = "https://www.youtube.com/embed/k88AjonUhMw"
            url_register = f'{url}{"LA500S"}'
            context = {
            "afiliado": None,
            "id":afiliado.fpa,
            "url_video": url_video_insercion,
            "url_register": url_register,
            
            }

        return render(request, 'index.html', context)

    except Usuario.DoesNotExist or Usuario.NoneType:
        return redirect('home')

   
def broker_pk(request,pk):
    try:
        afiliado = Usuario.objects.get(fpa=pk)
        url = f'/registro/{pk}'
        context = {
        "afiliado": afiliado,
        "id":afiliado.fpa,
        "url_register": url
        }

        return render(request,'broker.html',context)
    except Usuario.DoesNotExist or Usuario.NoneType:
        return redirect('broker_skilling')
    
    


def presenciales_pk(request,pk):
    try:
        afiliado = Usuario.objects.get(fpa=pk)
        url = f'/registro/{pk}'
        context = {
        "afiliado": afiliado,
        "id":afiliado.fpa,
        "url_register": url
        }
        return render(request, "presenciales.html",context)
    except Usuario.DoesNotExist or Usuario.NoneType:
        return redirect('presenciales')
    

def servicios_pk(request,pk):
    try:
        afiliado = Usuario.objects.get(fpa=pk)
        url = f'/registro/{pk}'
        context = {
        "afiliado": afiliado,
        "id":afiliado.fpa,
        "url_register": url
        }
        return render(request, "servicios.html",context)
    except Usuario.DoesNotExist or Usuario.NoneType:
        return redirect('servicios')
    
    
    
@csrf_exempt 
def consultaForm(request):
    if request.method == "POST":
        data = json.loads(request.body)

        nombre = data['nombre']
        telefono = data['telefono']
        correo = data['email']
        consulta = data['consulta']
        ubicacion = data['ubicacion']
        id_user = data['id_user']

        # Enviar correo electrónico usando los datos extraídos
        enviar_correo(nombre, telefono, correo, consulta, ubicacion, id_user)

        return JsonResponse({'message': 'Consulta enviada correctamente','status':200}, status=200)
    
    


######################################### Metodos ayudas #############################################33

    
def enviar_correo(nombre, telefono, correo, consulta, ubicacion, id_user):
    asunto = 'Consulta desde la página web'
    mensaje = f"Nombre: {nombre} {telefono}\nCorreo electrónico: {correo}\nConsulta:\n{consulta} \nUbicacion: {ubicacion} \nId User: {id_user}"
    lista_destinatarios = ['livecommunity.adm@gmail.com']  # Reemplaza con tu correo electrónico de destinatario
    correo_remitente = 'livecommunity.adm@gmail.com'  # Igual que EMAIL_HOST_USER

    send_mail(asunto, mensaje, correo_remitente, lista_destinatarios)
    
    


def convertir_url_youtube(url_original):
    if 'youtu.be/' in url_original:
        # URL corta de YouTube (youtu.be)
        video_id = url_original.split('youtu.be/')[-1]
    elif 'youtube.com/' in url_original and 'v=' in url_original:
        # URL normal de YouTube
        video_id = url_original.split('v=')[-1].split('&')[0]
    else:
        # Si no es una URL de YouTube reconocida, devuelve la URL original
        return url_original

    # Construye la URL de inserción
    url_insercion = f'https://www.youtube.com/embed/{video_id}'
    return url_insercion


def registro(request):
    return render(request, 'index.html')


def registro_form(request, pk):
    
    if pk is None:
        return redirect('home')
    
    afiliado = Usuario.objects.get(fpa=pk)
    context = {
        'afiliado': afiliado,
        'pk': pk
    }
    
    return render(request, 'registro.html', context)




