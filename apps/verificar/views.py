import os
import tempfile
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from .models import Archivo,Verificar
from django.contrib import admin
import pandas as pd
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


#######Metodo anterior
# def obtenerLosId(data):
#     ids = data['generic1']
#     dataFrame = ids.to_list()
#     dataFrame = [str(element) for element in dataFrame]
#     newList = []
#     for i in dataFrame:
#         if i and i != 'nan':
#             if ',' in i:
#                 primerId = i.split(',')[0]
#                 newList.append(primerId)
#             else:
#                 newList.append(i)
    
#     return list(set(newList))

# def obtenerDosColumnas(data):
#     columnas = data[['generic1', 'Net Deposits']]
#     dataFrame = columnas.dropna(subset=['generic1', 'Net Deposits']).values.tolist()
#     for i in range(len(dataFrame)):
#         dataFrame[i][0] = dataFrame[i][0].split(',')[0]
#         if dataFrame[i][1] != 0:
#             dataFrame[i][1] = 1
#         for j in range(len(dataFrame)):
#             if dataFrame[i][1] == 1 and dataFrame[i][0] == dataFrame[j][0]:
#                 dataFrame[j][1] = dataFrame[i][1]
#     return dataFrame

####################### Nuevo codigo para testear #####################
def retornarCorrecto(data):
    
    for i in range(len(data)):
        data[i][0] = data[i][0].split(',')
        for j in range(len(data[i][0])):
            if int(data[i][0][j]) >=1800000000:
                data[i][0] = data[i][0][j]
    return data

def obtenerDosColumnas(data):
    columnas = data[['generic1', 'Net Deposits']]
    dataFrame = columnas.dropna(subset=['generic1', 'Net Deposits']).values.tolist()
    
    dataFrame = retornarCorrecto(dataFrame)
    
    for i in range(len(dataFrame)):
        dataFrame[i][0] = dataFrame[i][0].split(',')[0]
        if dataFrame[i][1] != 0:
            dataFrame[i][1] = 1
        for j in range(len(dataFrame)):
            if dataFrame[i][1] == 1 and dataFrame[i][0] == dataFrame[j][0]:
                dataFrame[j][1] = dataFrame[i][1]
                
                
    print(dataFrame)
    return dataFrame

def filtrarPorSegundoValorNoCero(arr):
    resultado = []
    for elemento in arr:
        if elemento[1] != 0:
            resultado.append(elemento)
    print(resultado)
    return resultado

def existe(valor,ids):
    for client in ids:
        if client.id == valor[0]:
            return True
        
        
@csrf_exempt        
def verificar(request):
    idCli = Verificar.objects.all()
    
    data = []
    
    for i in idCli:
        data.append([i.id,i.deposito])
    
    response = JsonResponse({'data': data})
    response['Access-Control-Allow-Origin'] = '*'  # Permitir acceso desde cualquier origen
    
    return response


class ArchivoAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        ban = True
        archivo = form.cleaned_data['archivo']
        print(archivo)
        # Procesar el archivo Excel y obtener la columna deseada
        contenido = pd.read_excel(archivo,engine='openpyxl')
        ids = obtenerDosColumnas(contenido)
        idEnVerificar = Verificar.objects.all()
    
        print(ids)
        # Guardar los ids en la base de datos
        #
        #
        ############Aca esta el error ################
        for valor in ids:
            if not existe(valor,idEnVerificar):
                objeto = Verificar(id=valor[0],deposito=valor[1])
                objeto.save()
            else:
                ban = False
                obj = Verificar.objects.get(id = valor[0])
                obj.deposito = valor[1]
                obj.save()

                
              
      
        
        
        super().save_model(request, obj, form, change)
        
        #Elimina archivo de la carpeta media
        if ban:
            media_path = os.path.join(settings.MEDIA_ROOT, 'media', archivo.name)
            os.remove(media_path)


##################### En prototipo#######################

    # def delete_model(self, request, obj):
    #     # Eliminar el archivo del sistema de archivos
    #     media_path = obj.archivo.path
    #     os.remove(media_path)
        
    #     super().delete_model(request, obj)