from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from ...utils.formulas import calcula_porcentaje_directo,calcular_porcentaje_indirecto
from ...utils.funciones import formatera_retiro
from ...usuarios.models import Spread
from ...api.models import Registros_ganancias,Registros_cpa