import os
import tempfile
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from .models import Archivo,Verificar
from django.contrib import admin
import pandas as pd
from django.conf import settings


def obtenerLosId(data):
    ids = data['generic1']
    dataFrame = ids.to_list()
    dataFrame = [str(element) for element in dataFrame]
    newList = []
    for i in dataFrame:
        if i and i != 'nan':
            if ',' in i:
                primerId = i.split(',')[0]
                newList.append(primerId)
            else:
                newList.append(i)
    
    return list(set(newList))

def existe(valor,ids):
    for client in ids:
        if client.id == valor:
            return True
        
        
        
def verificar(request):
    idCli = Verificar.objects.all()
    
    data = []
    
    for i in idCli:
        data.append(i.id)
    
    return JsonResponse({'data':data})


class ArchivoAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        archivo = form.cleaned_data['archivo']
        
        # Procesar el archivo Excel y obtener la columna deseada
        contenido = pd.read_excel(archivo,engine='openpyxl')
        ids = obtenerLosId(contenido)
        idEnVerificar = Verificar.objects.all()
    
    
        # Guardar los ids en la base de datos
        for valor in ids:
            if not existe(valor,idEnVerificar):
                objeto = Verificar(id=valor)
                objeto.save()
      
        
        
        super().save_model(request, obj, form, change)
        
        #Elimina archivo de la carpeta media
        media_path = os.path.join(settings.MEDIA_ROOT, 'media', archivo.name)
        os.remove(media_path)


##################### En prototipo#######################

    # def delete_model(self, request, obj):
    #     # Eliminar el archivo del sistema de archivos
    #     media_path = obj.archivo.path
    #     os.remove(media_path)
        
    #     super().delete_model(request, obj)