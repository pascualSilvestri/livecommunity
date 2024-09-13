from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
import json 
from datetime import datetime
from django.db.models import Q
from ...skilling.models import Registro_archivo,Registros_ganancias,Relation_fpa_client


"""

Codigo que se tiene que verificar en caso de que la api de skilling nos llegue a funcionar podriamos facilitar estes proceso

#############################################################################################################################

"""

@csrf_exempt 
def verificar(request):
    if request.method == 'GET':
        try:
            registros = Registro_archivo.objects.all()
            clients = registros.values_list('client', flat=True)

            # Obtener todos los Relation_fpa_client relacionados en una sola consulta
            fpa_clients = Relation_fpa_client.objects.filter(client__in=clients)

            # Construir un diccionario para acceso rápido
            fpa_dict = {f.client: f for f in fpa_clients}

            data = []
            for r in registros:
                fpa = fpa_dict.get(r.client)
                if fpa:
                    dep = '1' if r.primer_deposito > 0 else '0'
                    data.append({
                        'client': r.client,
                        'deposit': dep,
                        'full_name': fpa.full_name.strip().lower(),
                        'fpa': fpa.fpa
                    })

            return JsonResponse({'data': data})
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Método inválido'})
"""

El codigo de arriba esta enverificacion en caso de que la api de skilling nos llegue a funcionar podriamos facilitar estes proceso

#############################################################################################################################

"""


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
def getRegistroById(request, pk):
    if request.method == 'GET':
        try:
            customer = Relation_fpa_client.objects.filter(fpa=pk)
            data = []
            
            for r in customer:
                registros = Registro_archivo.objects.filter(client=r.client)
                nombres = Relation_fpa_client.objects.filter(client=r.client)
                registro = registros.first()
                
                # Si no se encuentra un registro, saltar esta iteración
                if registro is None:
                    continue
                
                # Verifica si hay nombres asociados
                if nombres.exists():
                    nombre = nombres[0].full_name
                else:
                    nombre = 'None'
                
                # Construye el objeto de datos para cada cliente
                data.append({
                    'id_usuario': r.client,
                    'fecha_registro': registro.fecha_registro,
                    'codigo': r.fpa,
                    'pais': registro.country,
                    'primer_deposito': registro.primer_deposito,
                    'deposito_neto': registro.neto_deposito,
                    'cantidad_deposito': registro.numeros_depositos,
                    'id_broker': registro.client,
                    'nombre': nombre
                })
            
            # Retorna los datos como respuesta JSON
            return JsonResponse({'data': data})
        
        except Exception as e:
            return JsonResponse({'Error': str(e)})
    
    else:
        return JsonResponse({'Error': 'Método inválido'})

@csrf_exempt
def filter_registros_fecha_by_id(request, pk, desde, hasta):
    try:
        if request.method == 'GET':
            # Filtrar registros por fecha y fpa
            registros = Registro_archivo.objects.filter(
                Q(fecha_registro__gte=desde) & Q(fecha_registro__lte=hasta), fpa=pk
            )

            data = []
            for r in registros:
                # Verifica si existen nombres asociados al cliente
                nombres = Relation_fpa_client.objects.filter(client=r.client)
                
                # Si no se encuentra un nombre, asigna 'None'
                if nombres.exists():
                    nombre = nombres[0].full_name
                else:
                    nombre = 'None'

                # Añade la información del registro a la lista de datos
                data.append({
                    'id_usuario': r.client,
                    'fecha_registro': r.fecha_registro,
                    'codigo': r.fpa,
                    'pais': r.country,
                    'primer_deposito': r.primer_deposito,
                    'deposito_neto': r.neto_deposito,
                    'cantidad_deposito': r.numeros_depositos,
                    'id_broker': r.client,
                    'nombre': nombre
                })

            # Retorna la respuesta con los datos
            return JsonResponse({'data': data})

    except Registro_archivo.DoesNotExist:
        return JsonResponse({'Error': 'No se encontraron registros para el rango de fechas proporcionado.'}, status=404)
    except ValueError:
        return JsonResponse({'Error': 'Formato de fecha inválido. Por favor usa el formato YYYY-MM-DD.'}, status=400)
    except Exception as e:
        return JsonResponse({'Error': str(e)}, status=500)

    # Si el método no es GET, retornar error
    return JsonResponse({'Error': 'Método HTTP inválido'}, status=405)
