from django.http import JsonResponse
from django.shortcuts import render
from apps.afiliado.models  import Afiliado


def home(request):

    url_video_insercion =convertir_url_youtube ("https://www.youtube.com/watch?v=HgKjhFEguyU")
    url_register = ""
    context = {
        "afiliado": None,
        "url_video": url_video_insercion,
        "url_register": url_register
    }
    return render(request, "index.html",context)


# PRIMER SPRIG
def broker(request):
    return render(request,'broker.html')


def presenciales(request):
    return render(request, "presenciales.html")


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
    try:
        afiliado = Afiliado.objects.get(fpa=pk)
    except Afiliado.DoesNotExist:
        afiliado = None

    if afiliado:
        url_video_insercion = convertir_url_youtube(afiliado.url_video)
        url_register = afiliado.url
        context = {
            "afiliado": afiliado,
            "url_video": url_video_insercion,
            "url_register": url_register
        }
    else:
        url_video_insercion = "https://www.youtube.com/watch?v=HgKjhFEguyU"
        url_register = "livecommunity.info"
        context = {
            "afiliado": None,
            "url_video": url_video_insercion,
            "url_register": url_register
        }

    return render(request, 'index.html', context)
