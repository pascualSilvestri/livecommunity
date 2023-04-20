from django.shortcuts import render
from .models import Afiliado

def afiliado(request, idAfiliado):
    
    afiliado = Afiliado.objects.get(idAfiliado = idAfiliado)
    
    context = {'afiliado':afiliado,'idAfiliado':idAfiliado}
    
    return render(request, 'afiliado.html', context)

def idAfi(request, idAfiliado):
    
    afiliado = Afiliado.objects.get(idAfiliado = idAfiliado)
    
    context = {'afiliado':afiliado,'idAfiliado':idAfiliado}
    
    
    return render(request,'form.html', context)