from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
import json 
from datetime import datetime
from django.db.models import Q, FloatField, IntegerField
from ...skilling.models import Registro_archivo,Registros_ganancias,Relation_fpa_client
from django.db.models import F, Value, OuterRef, Subquery
from django.db.models.functions import Coalesce
from django.views.decorators.http import require_GET

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
    try:
        # Subconsulta para obtener los datos del Registro_archivo
        registro_subquery = Registro_archivo.objects.filter(
            client=OuterRef('client')
        ).values('fecha_registro', 'country', 'primer_deposito', 'neto_deposito', 'numeros_depositos')[:1]

        # Consulta principal optimizada
        customers = Relation_fpa_client.objects.filter(fpa=pk).annotate(
            registro_fecha=Coalesce(Subquery(registro_subquery.values('fecha_registro')), Value(None)),
            registro_pais=Coalesce(Subquery(registro_subquery.values('country')), Value('')),
            registro_primer_deposito=Coalesce(Subquery(registro_subquery.values('primer_deposito')), Value(0.0), output_field=FloatField()),
            registro_deposito_neto=Coalesce(Subquery(registro_subquery.values('neto_deposito')), Value(0.0), output_field=FloatField()),
            registro_cantidad_deposito=Coalesce(Subquery(registro_subquery.values('numeros_depositos')), Value(0), output_field=IntegerField()),
        ).values(
            'client',
            'fpa',
            'full_name',
            'registro_fecha',
            'registro_pais',
            'registro_primer_deposito',
            'registro_deposito_neto',
            'registro_cantidad_deposito'
        )

        # Formatear los datos
        data = [
            {
                'id_usuario': c['client'],
                'fecha_registro': c['registro_fecha'],
                'codigo': c['fpa'],
                'pais': c['registro_pais'],
                'primer_deposito': c['registro_primer_deposito'],
                'deposito_neto': c['registro_deposito_neto'],
                'cantidad_deposito': c['registro_cantidad_deposito'],
                'id_broker': c['client'],
                'nombre': c['full_name'] or 'None'
            } for c in customers if c['registro_fecha'] is not None
        ]

        return JsonResponse({'data': data})

    except Exception as e:
        return JsonResponse({'Error': str(e)}, status=500)



@csrf_exempt
def filter_registros_fecha_by_id(request, pk, desde, hasta):
    try:
        # Subconsulta para obtener el nombre completo
        nombres_subquery = Relation_fpa_client.objects.filter(
            client=OuterRef('client')
        ).values('full_name')[:1]

        # Consulta principal optimizada
        registros = Registro_archivo.objects.filter(
            fecha_registro__range=(desde, hasta),
            fpa=pk
        ).annotate(
            nombre=Coalesce(Subquery(nombres_subquery), Value('None'))
        ).values(
            'client',
            'fecha_registro',
            'fpa',
            'country',
            'primer_deposito',
            'neto_deposito',
            'numeros_depositos',
            'nombre'
        )

        # Formatear los datos
        data = [
            {
                'id_usuario': r['client'],
                'fecha_registro': r['fecha_registro'],
                'codigo': r['fpa'],
                'pais': r['country'],
                'primer_deposito': r['primer_deposito'],
                'deposito_neto': r['neto_deposito'],
                'cantidad_deposito': r['numeros_depositos'],
                'id_broker': r['client'],
                'nombre': r['nombre']
            } for r in registros
        ]

        return JsonResponse({'data': data})

    except ValueError:
        return JsonResponse({'Error': 'Formato de fecha inválido. Por favor usa el formato YYYY-MM-DD.'}, status=400)
    except Exception as e:
        return JsonResponse({'Error': str(e)}, status=500)
