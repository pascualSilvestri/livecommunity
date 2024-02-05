from django.http import JsonResponse
from django.shortcuts import render, redirect
from apps.afiliado.models  import Afiliado


def home(request):

    url_video_insercion =convertir_url_youtube ("https://www.youtube.com/watch?v=HgKjhFEguyU")
    url_register = "https://livecommunity.info/Afiliado/LM500S"
    context = {
        "afiliado": None,
        "url_video": url_video_insercion,
        "url_register": url_register
    }
    return render(request, "index.html",context)


# PRIMER SPRIG
def broker_skilling(request):
    url_register = "https://livecommunity.info/Afiliado/LM500S"
    context ={
        "afiliado": None,
        "url_register": url_register
    }
    return render(request,'broker.html',context)


def presenciales(request):
    url_register = "https://livecommunity.info/Afiliado/LM500S"
    context ={
        "afiliado": None,
        "url_register": url_register
    }
    return render(request, "presenciales.html",context)


def servicios(request):
    url_register = "https://livecommunity.info/Afiliado/LM500S"
    context ={
        "afiliado": None,
        "url_register": url_register
    }
    return render(request, "servicios.html",context)


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
        if afiliado:
        # url_video_insercion = "https://www.youtube.com/watch?v=HgKjhFEguyU" if afiliado.url_video==0 or afiliado.url_video==''  else  convertir_url_youtube(afiliado.url_video) 
            url_video_insercion =convertir_url_youtube ("https://www.youtube.com/watch?v=HgKjhFEguyU")
            url_register = afiliado.url
            context = {
            "afiliado": afiliado,
            "id":afiliado.fpa,
            "url_video": url_video_insercion,
            "url_register": url_register
            }
        else:
            url_video_insercion = "https://www.youtube.com/watch?v=HgKjhFEguyU"
            url_register = "livecommunity.info"
            context = {
            "afiliado": None,
            "id":afiliado.fpa,
            "url_video": url_video_insercion,
            "url_register": url_register
            }

        return render(request, 'index.html', context)

    except Afiliado.DoesNotExist or Afiliado.NoneType:
        return redirect('home')

   
def broker_pk(request,pk):
    try:
        afiliado = Afiliado.objects.get(fpa=pk)
        url_register = afiliado.url
        context = {
        "afiliado": afiliado,
        "id":afiliado.fpa,
        "url_register": url_register
        }

        return render(request,'broker.html',context)
    except Afiliado.DoesNotExist or Afiliado.NoneType:
        return redirect('broker_skilling')
    
    


def presenciales_pk(request,pk):
    try:
        afiliado = Afiliado.objects.get(fpa=pk)
        url_register = afiliado.url
        context = {
        "afiliado": afiliado,
        "id":afiliado.fpa,
        "url_register": url_register
        }
        return render(request, "presenciales.html",context)
    except Afiliado.DoesNotExist or Afiliado.NoneType:
        return redirect('presenciales')
    
    


def servicios_pk(request,pk):
    try:
        afiliado = Afiliado.objects.get(fpa=pk)
        url_register = afiliado.url
        context = {
        "afiliado": afiliado,
        "id":afiliado.fpa,
        "url_register": url_register
        }
        return render(request, "servicios.html",context)
    except Afiliado.DoesNotExist or Afiliado.NoneType:
        return redirect('servicios')
    
    
