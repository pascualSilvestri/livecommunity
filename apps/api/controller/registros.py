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
                    data.append(
                        {
                            'client':r.client,
                            'deposit':str(dep),
                            'full_name':fpa.first().full_name.strip().lower(),
                            'fpa':fpa.first().fpa
                            }
                        )
            
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

# @csrf_exempt 
# def getRegistroById(request,pk):
    
#     if request.method == 'GET':
        
#         try:
#             registros = Registro_archivo.objects.filter(fpa=pk)
#             data=[]
#             for r in registros:
#                 nombres = Relation_fpa_client.objects.filter(client=r.client)
#                 if nombres.exists():
#                     nombre = nombres[0].full_name
#                 else:
#                     nombre = 'None'
#                 data.append(
#                     {'id_usuario':r.client,
#                     'fecha_registro':r.fecha_registro,
#                     'codigo':r.fpa,
#                     'pais':r.country,
#                     'primer_deposito':r.primer_deposito,
#                     'deposito_neto':r.neto_deposito,
#                     'cantidad_deposito':r.numeros_depositos,
#                     'id_broker':r.client,
#                     'nombre':nombre
#                     }
#                 )
            
#             response = JsonResponse({'data': data})
            
#             return response
        
#         except Exception:
#             return JsonResponse({'Error':str(Exception)})
#     else:
#         return JsonResponse({'Error':'Metodo invalido'})




@csrf_exempt 
def getRegistroById(request,pk):
    
    if request.method == 'GET':
        
        try:
            customer = Relation_fpa_client.objects.filter(fpa=pk)
            data=[]
            for r in customer:
                registros= Registro_archivo.objects.filter(client=r.client)
                registro = registros.first()
                if customer.exists():
                    nombre = nombres[0].full_name
                else:
                    nombre = 'None'
                
                data.append(
                    {'id_usuario':r.client,
                    'fecha_registro':registro.fecha_registro,
                    'codigo':r.fpa,
                    'pais':registro.country,
                    'primer_deposito':registro.primer_deposito,
                    'deposito_neto':registro.neto_deposito,
                    'cantidad_deposito':registro.numeros_depositos,
                    'id_broker':registro.client,
                    'nombre':nombre
                    }
                )
            
            response = JsonResponse({'data': data})
            
            return response
        
        except Exception:
            return JsonResponse({'Error':str(Exception)})
    else:
        return JsonResponse({'Error':'Metodo invalido'})
    


    
@csrf_exempt 
def filter_registros_fecha_by_id(request,pk,desde,hasta):
    
    # fecha_desde = datetime.strptime(desde, "%Y-%m-%d").date
    # fecha_hasta = datetime.strptime(hasta, "%Y-%m-%d").date
    
    try:
        if request.method == 'GET':
            registros = Registro_archivo.objects.filter(Q(fecha_registro__gte=desde) & Q(fecha_registro__lte=hasta),fpa=pk)
            
            data= []
            for r in registros:
                nombres = Relation_fpa_client.objects.filter(client=r.client)
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
            
            response = JsonResponse({'data':data})
            return response
        
    except ValueError:
        print(ValueError)
        return ValueError




# @csrf_exempt
# def filter_registros_fecha_by_id(request, pk, desde, hasta):
#     # fecha_desde = datetime.strptime(desde, "%Y-%m-%d").date
#     # fecha_hasta = datetime.strptime(hasta, "%Y-%m-%d").date

#     if request.method == "GET":
#         try:
#             customer = Relation_fpa_client.objects.filter(fpa=pk)
#             data = []
#             for r in customer:
#                 registros = Registro_archivo.objects.filter(
#                     Q(fecha_registro__gte=desde) & Q(fecha_registro__lte=hasta),
#                     client=r.client,
#                 )
#                 registro = registros.first()

#                 if registro is not None:
#                     data.append(
#                         {
#                             "id_usuario": r.client,
#                             "fecha_registro": registro.fecha_registro,
#                             "codigo": r.fpa,
#                             "pais": registro.country,
#                             "primer_deposito": registro.primer_deposito,
#                             "deposito_neto": registro.neto_deposito,
#                             "cantidad_deposito": registro.numeros_depositos,
#                             "id_broker": registro.client,
#                             "nombre": r.full_name,
#                         }
#                     )
#                 else:
#                     return JsonResponse({"Error": "No se encontraron registros"})

#                 response = JsonResponse({"data": data})

#                 return response

#         except Exception as e:
#             return JsonResponse({"Error": str(e)})
#     else:
#         return JsonResponse({"Error": "Metodo invalido"})
