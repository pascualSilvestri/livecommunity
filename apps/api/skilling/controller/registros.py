from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
import json 
from datetime import datetime
from django.db.models import Q, FloatField, IntegerField

from livecommunity import settings
from ...skilling.models import Registro_archivo,Registros_ganancias,Relation_fpa_client
from django.db.models import F, Value, OuterRef, Subquery
from django.db.models.functions import Coalesce
from django.views.decorators.http import require_GET
import requests

"""

Codigo que se tiene que verificar en caso de que la api de skilling nos llegue a funcionar podriamos facilitar estes proceso

#############################################################################################################################

"""


@csrf_exempt
def filter_registros_fecha_by_id(request, pk, desde, hasta):
    try:
        # Construir la URL
        url = f"https://go.skillingpartners.com/api/?command=registrations&fromdate={desde}&todate={hasta}&daterange=update\\fdd&userid=&json=1"
        headers = {
            'x-api-key': settings.SKILLING_API_KEY,
            'affiliateid': '35881',
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Procesar la respuesta JSON
        registrations = response.json().get('registrations', [])

        # Filtrar registros donde Tracking_Code es igual a pk
        registrations = [reg for reg in registrations if reg.get('Tracking_Code') == pk]

        # Obtener todos los client_numbers de una vez
        client_numbers = [
            reg['User_ID'].split('-')[-1] if '-' in reg['User_ID'] else reg['User_ID']
            for reg in registrations
        ]

        # Obtener todos los nombres de una sola consulta
        nombres = {
            rc.client: rc.full_name
            for rc in Relation_fpa_client.objects.filter(client__in=client_numbers)
        }

        # Procesar los datos
        data = [
            {
                'id_usuario': client_number,
                'fecha_registro': reg.get('Registration_Date', ''),
                'codigo': reg.get('Tracking_Code', ''),
                'pais': reg.get('Country', ''),
                'primer_deposito': reg.get('First_Deposit', 0),
                'status':reg.get('Status',''),
                'deposito_neto': reg.get('Net_Deposits', 0),
                'cantidad_deposito': reg.get('Deposit_Count', 0),
                'id_broker': client_number,
                'nombre': nombres.get(client_number, 'None')
            }
            for reg, client_number in zip(registrations, client_numbers)
        ]

        return JsonResponse({'data': data})

    except requests.RequestException as e:
        return JsonResponse({
            'error': str(e),
            'url': url,
            'status_code': e.response.status_code if e.response else None,
            'content': e.response.text if e.response else None
        }, status=500)
    except Exception as e:
        return JsonResponse({'Error': str(e)}, status=500)



@csrf_exempt
def proxy_request(request, pk):
    url = f"https://go.skillingpartners.com/api/?command=registrations&fromdate=&todate=&daterange=update&userid=skilling-{pk}&json=1"
    headers = {
        'x-api-key': settings.SKILLING_API_KEY,
        'affiliateid': '35881',
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Esto lanzará una excepción para códigos de estado HTTP no exitosos
        
        # Intentar decodificar la respuesta JSON
        try:
            json_response = response.json()
            return JsonResponse(json_response)
        except requests.exceptions.JSONDecodeError:
            # Si no se puede decodificar como JSON, devolver el contenido de texto
            return JsonResponse({
                'error': 'No se pudo decodificar la respuesta como JSON',
                'content': response.text,
                'status_code': response.status_code,
                'headers': dict(response.headers)
            })
    except requests.RequestException as e:
        return JsonResponse({
            'error': str(e),
            'url': url,
            'status_code': e.response.status_code if e.response else None,
            'content': e.response.text if e.response else None
        }, status=500)