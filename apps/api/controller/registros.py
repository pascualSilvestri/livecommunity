from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
import json 
from datetime import datetime
from django.db.models import Q
from ...api.models import Registro_archivo,Registros_ganancias,Relation_fpa_client

@csrf_exempt 
def verificar(request):
    if request.method=='GET':
        try:
            registros = Registro_archivo.objects.all()
            
            
            data = []
            
            for r in registros:
                fpa = Relation_fpa_client.objects.filter(client=r.client)
                dep = 0
                if r.primer_deposito>0:
                    dep = 1
                    if fpa.exists():
                        # data.append([r.client,str(dep),fpa.first().full_name.strip().lower(),fpa.first().fpa])
                        data.append({'client':r.client,'deposit':str(dep),'full_name':fpa.first().full_name.strip().lower(),'fpa':fpa.first().fpa})
            
            return JsonResponse({'data':data})
            
        except Exception as e:
            print(e)
    else:
        return JsonResponse({'error':'metodo invalido'})



def registrosGetAll(request):
    
    if request.method == 'GET':
        try:
            registros = Registro_archivo.objects.all()
            data=[]
            for r in registros:
                nombres = Registros_ganancias.objects.filter(client=r.client)
                if nombres.exists():
                    nombre = nombres[0].full_name
                else:
                    nombre = 'None'
                data.append(
                    {'id_usuario':r.client,
                    'fecha_registro':r.fecha_registro,
                    'codigo':r.fpa,
                    'pais':r.country,
                    'primer_deposito':r.primer_deposito,
                    'deposito_neto':r.neto_deposito,
                    'cantidad_deposito':r.numeros_depositos,
                    'id_broker':r.client,
                    'nombre':nombre
                    }
                )
            
            response = JsonResponse({'data': data})
            
            return response
        except Exception as e:
            return JsonResponse({'Error':e.__str__()})
    else:
            return JsonResponse({'Error':'Metodo invalido'})

@csrf_exempt 
def getRegistroById(request,pk):
    
    if request.method == 'GET':
        
        try:
            registros = Registro_archivo.objects.filter(fpa=pk)
            data=[]
            for r in registros:
                nombres = Registros_ganancias.objects.filter(client=r.client)
                if nombres.exists():
                    nombre = nombres[0].full_name
                else:
                    nombre = 'None'
                data.append(
                    {'id_usuario':r.client,
                    'fecha_registro':r.fecha_registro,
                    'codigo':r.fpa,
                    'pais':r.country,
                    'primer_deposito':r.primer_deposito,
                    'deposito_neto':r.neto_deposito,
                    'cantidad_deposito':r.numeros_depositos,
                    'id_broker':r.client,
                    'nombre':nombre
                    }
                )
            
            response = JsonResponse({'data': data})
            
            return response
        
        except Exception:
            return JsonResponse({'Error':str(Exception)})
    else:
        return JsonResponse({'Error':'Metodo invalido'})

# @csrf_exempt 
# def filterRegistrosFecha(request,desde,hasta):
    
#     # fecha_desde = datetime.strptime(desde, "%Y-%m-%d").date
#     # fecha_hasta = datetime.strptime(hasta, "%Y-%m-%d").date
    
#     try:
#         if request.method == 'GET':
#             registros = Registros.objects.filter(Q(fecha_registro__gte=desde) & Q(fecha_registro__lte=hasta))
            
#             data= []
#             for r in registros:
#                 data.append({
#                     'id_usuario': r.id_usuario,
#                     'fecha_registro':r.fecha_registro,
#                     'codigo': r.codigo,
#                     'pais' : r.pais,           
#                     'primer_deposito': r.primer_deposito,
#                     'retiro' : r.retiro,    
#                     'deposito_neto': r.deposito_neto,    
#                     'cantidad_deposito': r.cantidad_deposito,
#                     'id_broker' :r.id_broker ,
#                     'nombre' : r.nombre,
#                 })
            
#             response = JsonResponse({'data':data})
#             return response
        
#     except ValueError:
#         print(ValueError)
#         return ValueError


