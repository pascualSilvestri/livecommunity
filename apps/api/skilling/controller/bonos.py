from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import requests

from livecommunity import settings
from ....utils.formulas import calcula_porcentaje_directo, calcular_porcentaje_indirecto
from ....utils.funciones import formatera_retiro
from apps.api.skilling.models import (
    Spread,
    Cuenta,
    BonoAPagar,
    BonoCpa,
    BonoCpaIndirecto,
    CPA
)
from ...skilling.models import Registros_ganancias, Registros_cpa, Relation_fpa_client
import re
import json
from decimal import Decimal
import xml.etree.ElementTree as ET

def reseteo_bonos(request):
    if request.method == "GET":
        try:

            cuentas = Cuenta.objects.all()
            data = []
            for cuenta in cuentas:

                bonos_a_pagar = BonoAPagar(
                    fpa=cuenta.fpa,
                    monto_total=cuenta.monto_bono_directo + cuenta.monto_bono_indirecto,
                    monto_bono_indirecto=cuenta.monto_bono_indirecto,
                    monto_bono_directo=cuenta.monto_bono_directo,
                )
                cuenta.monto_a_pagar += (
                    cuenta.monto_bono_directo + cuenta.monto_bono_indirecto
                )
                cuenta.monto_bono_directo = 0
                cuenta.monto_bono_indirecto = 0
                cuenta.cpa_directo = 0
                cuenta.cpa_indirecto = 0
                cuenta.level_bono_directo = 0
                cuenta.level_bono_indirecto = 0
                cuenta.cpa = 0
                cuenta.cpaIndirecto = 0

                cuenta.save()
                bonos_a_pagar.save()

            data.append({"result": "ok", "status": 200, "data": "bonos guardados"})

            response = JsonResponse({"data": data})

            return response
        except Exception as e:
            return JsonResponse({"Error": str(e)})
    else:
        return JsonResponse({"Error": "Metodo invalidos"})


def get_bono_cpa(request):
    if request.method == "GET":
        try:

            bonoCpas = BonoCpa.objects.all()
            data = []
            for bonoCpa in bonoCpas:
                data.append({"valor": bonoCpa.valor, "bono": bonoCpa.bono})

            response = JsonResponse({"data": data})

            return response
        except Exception as e:
            return JsonResponse({"Error": str(e)})
    else:
        return JsonResponse({"Error": "Metodo invalidos"})


@csrf_exempt
def put_bono_cpa(request):
    if request.method == "PUT":
        try:
            body = json.loads(request.body)
            datos = body["data"]

            for dato in datos:
                bono = BonoCpa.objects.filter(bono=dato["bono"]).first()

                bono.valor = dato["valor"]
                bono.save()

            data = {"result": "ok", "status": 200, "data": "bonos guardados"}

            response = JsonResponse({"data": data})

            return response
        except Exception as e:
            return JsonResponse({"Error": str(e)})
    else:
        return JsonResponse({"Error": "Metodo invalidos"})


def get_bono_cpa_indirecto(request):
    if request.method == "GET":
        try:

            bonoCpas = BonoCpaIndirecto.objects.all()
            data = []
            for bonoCpa in bonoCpas:
                data.append({"valor": bonoCpa.valor, "bono": bonoCpa.bono})

            response = JsonResponse({"data": data})

            return response
        except Exception as e:
            return JsonResponse({"Error": str(e)})
    else:
        return JsonResponse({"Error": "Metodo invalidos"})


@csrf_exempt
def put_bono_cpa_indirecto(request):
    if request.method == "PUT":
        try:
            body = json.loads(request.body)
            datos = body["data"]

            print(datos)
            for dato in datos:
                bono = BonoCpaIndirecto.objects.filter(bono=dato["bono"]).first()

                bono.valor = dato["valor"]
                bono.save()

            data = {"result": "ok", "status": 200, "data": "bonos guardados"}

            response = JsonResponse({"data": data})

            return response
        except Exception as e:
            return JsonResponse({"Error": str(e)})
    else:
        return JsonResponse({"Error": "Metodo invalidos"})


def get_spread(request):
    if request.method == "GET":
        try:

            spreads = Spread.objects.all()
            data = []
            for spread in spreads:
                data.append({"porcentaje": spread.porcentaje, "spread": spread.spread})

            response = JsonResponse({"data": data})

            return response
        except Exception as e:
            return JsonResponse({"Error": str(e)})
    else:
        return JsonResponse({"Error": "Metodo invalidos"})


@csrf_exempt
def put_spread(request):
    if request.method == "PUT":
        try:
            body = json.loads(request.body)
            datos = body["data"]

            # print(datos)
            for dato in datos:
                spread = Spread.objects.filter(spread=dato["spread"]).first()
                spread.porcentaje = dato["porcentaje"]
                spread.save()
            data = {"result": "ok", "status": 200, "data": "bonos guardados"}

            response = JsonResponse({"data": data})

            return response
        except Exception as e:
            return JsonResponse({"Error": str(e)})
    else:
        return JsonResponse({"Error": "Metodo invalidos"})

@csrf_exempt
def create_allbonos(request):
    if request.method == "GET":
        try:
            # Diccionario con los valores de bonos indirectos
            bono_indirectos = {
                "level1": 100,
                "level2": 200,
                "level3": 400,
                "level4": 600,
                "level5": 1000,
                "level6": 2000,
                "level7": 3000,
                "level8": 4000,
            }

            # Diccionario con los valores de bonos directos
            bono_directos = {
                "level1": 50,
                "level2": 100,
                "level3": 150,
                "level4": 200,
                "level5": 300,
                "level6": 500,
                "level7": 700,
                "level8": 1000,
                "level9": 1500,
                "level10": 2000,
            }
            
            
            spread = {
                "spread_socio": 25.0,
                "spread_directo": 12.5,
                "spread_indirecto":10.0
                
            }

            # Guardar bonos indirectos en la base de datos
            for i in bono_indirectos.keys():
                
                bono = BonoCpaIndirecto(bono=i, valor=bono_indirectos[i])
                bono.save()

            # Guardar bonos directos en la base de datos
            for i in bono_directos.keys():
            
                bono = BonoCpa(bono=i, valor=bono_directos[i])
                bono.save()
            
            for i in spread.keys():
            
                bono = Spread(spread=i, porcentaje=spread[i])
                bono.save()
            
            CPA(cpa=60).save()
            # Respuesta de éxito
            data = {"result": "ok", "status": 200, "data": "bonos creados"}
            response = JsonResponse({"data": data})
            return response
        
        except Exception as e:
            # Manejo de errores
            return JsonResponse({"Error": str(e)})
    else:
        # Respuesta si el método no es PUT
        return JsonResponse({"Error": "Metodo inválido"})


    """
    Nuevo codigo para la creacion de bonos
    
    """
    
    
@csrf_exempt
def obtener_comisiones_by_date_by_id(request, pk, desde, hasta):
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

        return JsonResponse({'data': data})

    except requests.RequestException as e:
        return JsonResponse({
            'error': str(e),
            'url': url,
            'status_code': getattr(e.response, 'status_code', None),
            'content': getattr(e.response, 'text', None)
        }, status=500)
    except ET.ParseError:
        return JsonResponse({'Error': 'Error al analizar el XML recibido'}, status=500)
    except Exception as e:
        return JsonResponse({'Error': str(e)}, status=500)