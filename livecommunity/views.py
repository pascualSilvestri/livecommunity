from django.http import JsonResponse
from django.shortcuts import render
from apps.afiliado.models  import Afiliado


def Home(request):
    return render(request, "index.html")


# PRIMER SPRIG
def broker(request):
    return render(request, "inprocess.html")


def presenciales(request):
    return render(request, "inprocess.html")


def servicios(request):
    return render(request, "inprocess.html")


# def Broker(request):
#     return render(request,'broker.html')

# def Presenciales(request):
#     return render(request,'presenciales.html')

# def Servicios(request):
#     return render(request,'servicios.html')


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


def home_pk(request, pk):
    afiliado = Afiliado.objects.get(fpa=pk)
    url_video_insercion = convertir_url_youtube(afiliado.url_video)

    context = {"afiliado": afiliado, "url_video": url_video_insercion}
 
    # return JsonResponse(data)

    return render(request,'index.html',context)
