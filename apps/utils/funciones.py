from datetime import datetime
from livecommunity import settings
from ..api.skilling.models import Registros_ganancias, Relation_fpa_client
from django.db.models import Q, QuerySet
import requests  # Añadir esta línea para importar requests
import xml.etree.ElementTree as ET  # Añadir esta línea

def existe(client,fecha_registro,fpa,status,fecha_calif,country,posicion_cuenta,fecha_primer_deposito,neto_deposito,numeros_depositos,registros):
    
    for r in registros:
        if(client==r.client and fecha_registro == r.fecha_registro and fpa == r.fpa and status ==  r.status and fecha_calif == r.fecha_calif and country == r.country and posicion_cuenta == r.posicion_cuenta and fecha_primer_deposito == r.fecha_primer_deposito and neto_deposito == r.neto_deposito and numeros_depositos == r.numeros_depositos):
            return True
    return False


def existe_cpa(fecha,monto,client,fpa,cpas):
    for c in cpas:
        if (fecha==c.fecha_creacion and monto == c.monto and client == c.client and fpa == c.fpa):
            return True
    return False

def existe_ganancia(ganancia: Registros_ganancias, ganancias_existentes: QuerySet) -> bool:
    return ganancias_existentes.filter(
        Q(client=ganancia.client) &
        Q(fpa=ganancia.fpa) &
        Q(partner_earning=ganancia.partner_earning) &
        Q(fecha_operacion=ganancia.fecha_operacion) &
        Q(deal_id=ganancia.deal_id) &
        Q(position=ganancia.position)
    ).exists()

def formatera_retiro(valor):
    retiro = valor.replace('(','').strip()
    retiro = retiro.replace(')','').strip()
    retiro = retiro.split(' ')
    
    return retiro

def obtener_comisiones_api_skilling_by_id(pk, desde, hasta):
    try:
        url = f"https://go.skillingpartners.com/api/?command=commissions&fromdate={desde}&todate={hasta}"
        headers = {
            'x-api-key': settings.SKILLING_API_KEY,
            'affiliateid': '35881',
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        root = ET.fromstring(response.content)

        data = []
        client_numbers = set()

        for commission in root.findall('Commission'):
            tracking_code = commission.find('TrackingCode').text
            if tracking_code != pk:
                continue

            trader_id = commission.find('TraderId').text
            client_number = trader_id.split('-')[-1] if '-' in trader_id else trader_id
            client_numbers.add(client_number)

            data.append({
                'commission_id': commission.find('id').text,
                'id_usuario': client_number,
                'codigo': tracking_code,
                'tipo_comision': commission.find('CommissionType').text,
                'comision': commission.find('Commission').text,
                'fecha_creacion': commission.find('created').text,
                'nombre': ''
            })

        nombres = dict(Relation_fpa_client.objects.filter(client__in=client_numbers).values_list('client', 'full_name'))

        for item in data:
            item['nombre'] = nombres.get(item['id_usuario'], 'None')

        return {'data': data}  # Retorna un diccionario en lugar de JsonResponse

    except requests.RequestException as e:
        return {
            'error': str(e),
            'url': url,
            'status_code': getattr(e.response, 'status_code', None),
            'content': getattr(e.response, 'text', None)
        }
    except ET.ParseError:
        return {'Error': 'Error al analizar el XML recibido'}
    except Exception as e:
        return {'Error': str(e)}
    
    
    
def obtener_comisiones_api_skilling(desde, hasta):
    try:
        url = f"https://go.skillingpartners.com/api/?command=commissions&fromdate={desde}&todate={hasta}"
        headers = {
            'x-api-key': settings.SKILLING_API_KEY,
            'affiliateid': '35881',
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        root = ET.fromstring(response.content)

        data = []
        client_numbers = set()

        for commission in root.findall('Commission'):
            tracking_code = commission.find('TrackingCode').text

            trader_id = commission.find('TraderId').text
            client_number = trader_id.split('-')[-1] if '-' in trader_id else trader_id
            client_numbers.add(client_number)

            data.append({
                'commission_id': commission.find('id').text,
                'id_usuario': client_number,
                'codigo': tracking_code,
                'tipo_comision': commission.find('CommissionType').text,
                'comision': commission.find('Commission').text,
                'fecha_creacion': commission.find('created').text,
                'nombre': ''
            })

        nombres = dict(Relation_fpa_client.objects.filter(client__in=client_numbers).values_list('client', 'full_name'))

        for item in data:
            item['nombre'] = nombres.get(item['id_usuario'], 'None')

        return data  # Retorna un diccionario en lugar de JsonResponse

    except requests.RequestException as e:
        return {
            'error': str(e),
            'url': url,
            'status_code': getattr(e.response, 'status_code', None),
            'content': getattr(e.response, 'text', None)
        }
    except ET.ParseError:
        return {'Error': 'Error al analizar el XML recibido'}
    except Exception as e:
        return {'Error': str(e)}
    
def parse_date(date_string):
    if date_string == "nan":
        return None
    return datetime.strptime(date_string, "%Y-%m-%d").date()
