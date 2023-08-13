from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from ...utils.formulas import calcula_porcentaje_directo,calcular_porcentaje_indirecto
from ...usuarios.models import Spread

@csrf_exempt  
def gananciaGetAll(request):
    
    if request.method == 'GET':
        try:
            ganancias = Ganancia.objects.all()
            
            data=[]
            
            for r in ganancias:
                data.append( 
                    {
                        'creacion':r.creacion,
                        'monto':r.monto,
                        'monto_spread':r.monto_spread,
                        'tipo_comision':r.tipo_comision,
                        'id_usuario':r.id_usuario,
                        'codigo':r.codigo,
                        'isPago':r.pagado
                    }
                )
            
            response = JsonResponse({'data': data})
            
            return response
        except Exception:
            return JsonResponse({'Error':str(Exception)})
    else:
        return JsonResponse({'Error':'Metodo invalidos'})

@csrf_exempt
def getRGananciasById(request,pk):
    
    if request.method == 'GET':
        
        try:
                
            ganancias = Ganancia.objects.filter(codigo=pk)
            
            data=[]
            
            for r in ganancias:
                data.append( 
                    {
                        'creacion':r.creacion,
                        'monto':r.monto,
                        'monto_spread':r.monto_spread,
                        'tipo_comision':r.tipo_comision,
                        'id_usuario':r.id_usuario,
                        'codigo':r.codigo,
                        'isPago':r.pagado
                    }
                )
            
            response = JsonResponse({'data': data})

            return response
        except Exception:
            return JsonResponse({'Error':str(Exception)})
    else:
        return JsonResponse({'Error':'Metodo invalidos'})

@csrf_exempt  
def gananciasTotales(request):
    
    if request.method == 'GET':
        try:
            ganancias = Ganancia.objects.all()
            
            total = 0
            
            for m in ganancias:
                total += m.monto
            
            response = JsonResponse({'monto':total})
            
            return response
        except Exception:
            return JsonResponse({'Error':str(Exception)})
    else:
        return JsonResponse({'Error':'Metodo invalidos'})


@csrf_exempt  
def gananciasTotalUser(request,pk):
    
    if request.method == 'GET':
        try:
            
            ganancias = Ganancia.objects.filter(codigo=pk)
            
            total = 0
            
            for m in ganancias:
                total += m.monto
            
            response = JsonResponse({'monto':total})
            
            return response
        except Exception:
            return JsonResponse({'Error':str(Exception)})
    else:
        return JsonResponse({'data':'El metodo es invalido'})


@csrf_exempt  
def filtarGananciasCpa(request):
    
    if request.method == "GET":    
        try:
            ganancias = Ganancia.objects.filter(tipo_comision='CPA')
            data=[]
            for r in ganancias:
                data.append( 
                    {
                        'creacion':r.creacion,
                        'monto':r.monto,
                        'monto_spread':r.monto_spread,
                        'tipo_comision':r.tipo_comision,
                        'id_usuario':r.id_usuario,
                        'codigo':r.codigo,
                        'isPago':r.pagado
                    }
                )
            response = JsonResponse({'data':data})
            return response

        except Exception:
            return JsonResponse({'error': str(Exception)})
    else:
        return JsonResponse({'error':'The method is invalid'})

@csrf_exempt  
def filtarGananciasCpaById(request,pk):
    if request.method == "GET":    
        try:
            ganancias = Ganancia.objects.filter(tipo_comision='CPA',codigo=pk)
            data=[]
            for r in ganancias:
                data.append( 
                    {
                        'creacion':r.creacion,
                        'monto':r.monto,
                        'monto_spread':r.monto_spread,
                        'tipo_comision':r.tipo_comision,
                        'id_usuario':r.id_usuario,
                        'codigo':r.codigo,
                        'isPago':r.pagado
                    }
                )
            response = JsonResponse({'data':data})
            return response

        except Exception:
            return JsonResponse({'error': str(Exception)})
    else:
        return JsonResponse({'error':'The method is invalid'})
    
@csrf_exempt  
def filtradoGananciasRevshare(request):
    
    if request.method == 'GET':
        try:
            
            ganancias = Ganancia.objects.filter(tipo_comision='Revshare')
            
            data = []
            
            for r in ganancias:
                data.append( 
                    {
                        'creacion':r.creacion,
                        'monto':r.monto,
                        'monto_spread':r.monto_spread,
                        'tipo_comision':r.tipo_comision,
                        'id_usuario':r.id_usuario,
                        'codigo':r.codigo,
                        'isPago':r.pagado
                    }
                )
            
            return JsonResponse({'data':data})
        
        except Exception:
            return JsonResponse({'Error':Exception})
    else:
        return JsonResponse({'Error':'Metodo invalido'})


def filtradoGananciasRevshareById(request,pk):
    
    if request.method == 'GET':
        try:
            
            ganancias = Ganancia.objects.filter(tipo_comision='Revshare',codigo=pk)
            
            data = []
            
            for r in ganancias:
                data.append( 
                    {
                        'creacion':r.creacion,
                        'monto':r.monto,
                        'monto_spread':r.monto_spread,
                        'tipo_comision':r.tipo_comision,
                        'id_usuario':r.id_usuario,
                        'codigo':r.codigo,
                        'isPago':r.pagado
                    }
                )
            
            return JsonResponse({'data':data})
        
        except Exception:
            return JsonResponse({'Error':Exception})
    else:
        return JsonResponse({'Error':'Metodo invalido'})


def filterGananciasFecha(request,desde,hasta):
    
    # fecha_desde = datetime.strptime(desde, "%Y-%m-%d").date
    # fecha_hasta = datetime.strptime(hasta, "%Y-%m-%d").date
    
    try:
        if request.method == 'GET':
            ganancias = Ganancia.objects.filter(Q(creacion__gte=desde) & Q(creacion__lte=hasta))
            
            data= []
            for r in ganancias:
                data.append( 
                    {
                        'creacion':r.creacion,
                        'monto':r.monto,
                        'monto_spread':r.monto_spread,
                        'tipo_comision':r.tipo_comision,
                        'id_usuario':r.id_usuario,
                        'codigo':r.codigo,
                        'isPago':r.pagado
                    }
                )
            
            
            response = JsonResponse({'data':data})
            return response
        
    except ValueError:
        print(ValueError)
        return ValueError


def filter_ganancia_to_date_by_id(request,pk,desde,hasta):
    
    # fecha_desde = datetime.strptime(desde, "%Y-%m-%d").date
    # fecha_hasta = datetime.strptime(hasta, "%Y-%m-%d").date
    spread = Spread.objects.all()
    try:
        if request.method == 'GET':
            ganancias = Ganancia.objects.filter(Q(creacion__gte=desde) & Q(creacion__lte=hasta),codigo=pk,pagado=False)
            
            data= []
            monto_a_pagar=0
            for r in ganancias:
                monto_a_pagar += calcula_porcentaje_directo(r.monto,spread[0].porcentaje,spread[1].porcentaje)
                
            data.append( 
                    {
                        'monto': round(monto_a_pagar,2)
                    }
                )
            
            
            response = JsonResponse({'data':data})
            return response
        
    except ValueError:
        print(ValueError)
        return ValueError