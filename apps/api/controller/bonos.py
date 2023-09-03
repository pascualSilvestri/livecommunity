from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from ...utils.formulas import calcula_porcentaje_directo,calcular_porcentaje_indirecto
from ...utils.funciones import formatera_retiro
from ...usuarios.models import Spread,Usuario,Cuenta,BonoAPagar
from ...api.models import Registros_ganancias,Registros_cpa
import re
import json 
from decimal import Decimal



def reseteo_bonos(request):
    if request.method == 'GET':
        try:
            
            cuentas = Cuenta.objects.all()
            data= []
            for cuenta in cuentas:
                
                bonos_a_pagar = BonoAPagar(
                    fpa = cuenta.fpa,
                    monto_total = cuenta.monto_bono_directo+ cuenta.monto_bono_indirecto,
                    monto_bono_indirecto =cuenta.monto_bono_indirecto ,
                    monto_bono_directo = cuenta.monto_bono_directo,
                )
                cuenta.monto_a_pagar += (cuenta.monto_bono_directo + cuenta.monto_bono_indirecto)
                cuenta.monto_bono_directo = 0
                cuenta.monto_bono_indirecto = 0
                cuenta.cpa_directo = 0
                cuenta.cpa_indirecto = 0
                cuenta.level_bono_directo = 0
                cuenta.level_bono_indirecto = 0 
                cuenta.cpa= 0
                cuenta.cpaIndirecto = 0
                
                cuenta.save() 
                bonos_a_pagar.save()
                
            data.append({
                'result':'ok',
                'status':200,
                'data':'bonos guardados'
            })

            
            response = JsonResponse({'data': data})
            
            return response
        except Exception as e:
            return JsonResponse({'Error':str(e)})
    else:
        return JsonResponse({'Error':'Metodo invalidos'})