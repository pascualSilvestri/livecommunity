from django.shortcuts import render
from .models import Afiliado,Cliente
from .forms import ClienteForm
from django.core.exceptions import ObjectDoesNotExist
import os
from django.conf import settings
from django.urls import reverse_lazy


def afiliado(request, idAfiliado):
    afiliado = False
    try:
        afiliado = Afiliado.objects.get(idAfiliado=idAfiliado)
        form = ClienteForm()
        context = {'afiliado': afiliado, 'idAfiliado': idAfiliado, 'form': form}
        return render(request, 'afiliado.html', context)
    except ObjectDoesNotExist:
        afiliado = False
        return render(request, 'error.html')

   


def idAfi(request, idAfiliado):
    
    afiliado = Afiliado.objects.get(idAfiliado = idAfiliado)
    
    context = {'afiliado':afiliado,'idAfiliado':idAfiliado}
    
    
    return render(request,'form.html', context)


def clienteform(request):
    if request.method == 'POST':
        
        # Obtener los demás datos del formulario
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        idAfiliado = request.POST.get('idAfiliado')
        userTelegram = request.POST.get('userTelegram')
        
        # Crear un objeto de modelo con los datos del formulario, incluyendo la ruta del archivo
        cliente = Cliente(
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            telefono=telefono,
            idAfiliado=idAfiliado,
            userTelegram=userTelegram
        )
        cliente.save()  # Guardar el objeto en la base de datos
        
    return render(request, 'linkGrupos.html')
