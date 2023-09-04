from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from ...utils.formulas import calcula_porcentaje_directo,calcular_porcentaje_indirecto
from ...utils.funciones import formatera_retiro
from ...usuarios.models import Spread
from ...api.models import Registros_ganancias,Registros_cpa
from ...usuarios.models import Cuenta

@csrf_exempt  
def montosGet(request,pk):

    if request.method == 'GET':
        try:
            
            usuario = Cuenta.objects.get(fpa=pk)
            
            data = [{
                "monto_total":usuario.monto_total,
                "monto_a_pagar":usuario.monto_a_pagar,
                "monto_cpa":usuario.monto_cpa,
                "monto_directo":usuario.cpa_directo,
                "monto_indirecto":usuario.cpa_indirecto,
                "monto_bono_directo":usuario.monto_bono_directo,
                "monto_bono_indirecto":usuario.monto_bono_indirecto,
                "cpa_directos":usuario.cpa,
                "cpa_indirecto":usuario.cpaIndirecto,
                "level_bono_directo": usuario.level_bono_directo,
                "level_bono_indirecto": usuario.level_bono_indirecto,
            }]
            
            return JsonResponse({"data":data})
            
        except Exception as e:
            return JsonResponse({'Error':e})
    else:
        return JsonResponse({'Error':'Metodo Incorrecto'})

