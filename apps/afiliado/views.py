from django.shortcuts import render
from .models import Afiliado,Cliente
from .forms import ClienteForm
import os
from django.conf import settings

def afiliado(request, idAfiliado):
    
    afiliado = Afiliado.objects.get(idAfiliado = idAfiliado)
    form = ClienteForm()
    
    context = {'afiliado':afiliado,'idAfiliado':idAfiliado,'form':form}
    
    return render(request, 'afiliado.html', context)

def idAfi(request, idAfiliado):
    
    afiliado = Afiliado.objects.get(idAfiliado = idAfiliado)
    
    context = {'afiliado':afiliado,'idAfiliado':idAfiliado}
    
    
    return render(request,'form.html', context)


def clienteform(request):
    if request.method == 'POST':
        # Obtener el archivo del formulario
        comprobante = request.FILES.get('comprobante')
        
        # Obtener la ruta de destino para guardar el archivo
        file_path = os.path.join(settings.MEDIA_ROOT, comprobante.name)
        
        # Guardar el archivo en la ruta de destino
        with open(file_path, 'wb') as file:
            for chunk in comprobante.chunks():
                file.write(chunk)
        
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
            comprobante=file_path.replace(settings.MEDIA_ROOT, ''),
            idAfiliado=idAfiliado,
            userTelegram=userTelegram
        )
        cliente.save()  # Guardar el objeto en la base de datos
        
    return render(request, 'afiliado.html')



# def clienteform(request):

#     if request.method == 'POST':
#         nombre = request.POST.get('nombre')
#         apellido = request.POST.get('apellido')
#         correo = request.POST.get('correo')
#         telefono = request.POST.get('telefono')
#         comprobante = request.POST.get('comprobante')
#         idAfiliado = request.POST.get('idAfiliado')
#         userTelegram = request.POST.get('userTelegram')
        
        
        
#         cliente = Cliente(
#             nombre=nombre,
#             apellido=apellido,
#             correo=correo,
#             telefono=telefono,
#             comprobante=comprobante,
#             idAfiliado=idAfiliado,
#             userTelegram=userTelegram,
#             )
#         cliente.save()
        
#     return render(request,'afiliado.html')