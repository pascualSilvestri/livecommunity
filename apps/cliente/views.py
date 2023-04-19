from django.shortcuts import render
from .models import Cliente

def cliente(request, idCliente):
    
    cliente = Cliente.objects.get(idCliente = idCliente)
    
    context = {'cliente':cliente,'idCliente':idCliente}
    
    return render(request, 'hero.html', context)