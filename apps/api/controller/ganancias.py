from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from ...utils.formulas import calcula_porcentaje_directo,calcular_porcentaje_indirecto
from ...utils.funciones import formatera_retiro
from ...usuarios.models import Spread
from ...api.models import Registros_ganancias,Registros_cpa
import re

@csrf_exempt  
def ganancia_get_all(request):
    
    if request.method == 'GET':
        try:
            ganancias = Registros_ganancias.objects.all()
            cpas = Registros_cpa.objects.all()
            spred = Spread.objects.all()
            data=[]
            for r in ganancias:
                if r.pagado == False:
                    if r.partner_earning != 0:
                        monto_spread = round(calcula_porcentaje_directo(float(r.partner_earning),spred[0].porcentaje,spred[1].porcentaje),2)
                    else:
                        monto_spread = r.partner_earning
                    data.append( 
                        {
                            'creacion':r.fecha_first_trade,
                            'monto':r.partner_earning,
                            'monto_spread':monto_spread,
                            'tipo_comision':'Reverashe',
                            'client':r.client,
                            'retiro':r.withdrawals,
                            'isPago':r.pagado
                        }
                    )
            for c in cpas:
                data.append( 
                        {
                            'creacion':c.fecha_creacion,
                            'monto':c.monto,
                            'monto_spread':c.monto,
                            'tipo_comision':'CPA',
                            'client':c.client,
                            'retiro':0,
                            'isPago':c.pagado
                        }
                    )
            
            response = JsonResponse({'data': data})
            
            return response
        except Exception as e:
            return JsonResponse({'Error':e.__str__()})
    else:
        return JsonResponse({'Error':'Metodo invalidos'})


@csrf_exempt  
def ganancia_only_more_cero(request):
    
    if request.method == 'GET':
        try:
            ganancias = Registros_ganancias.objects.all()
            spred = Spread.objects.all()
            # cpas = Registros_cpa.objects.all()
            data=[]
            for r in ganancias:
                if r.pagado == False and r.partner_earning != 0:
                    if r.partner_earning != 0:
                        monto_spread = round(calcula_porcentaje_directo(float(r.partner_earning),spred[0].porcentaje,spred[1].porcentaje),2)
                    else:
                        monto_spread = r.partner_earning
                    data.append( 
                        {
                            'creacion':r.fecha_first_trade,
                            'monto':r.partner_earning,
                            'monto_spread':monto_spread,
                            'tipo_comision':'Reverashe',
                            'client':r.client,
                            'retiro':r.withdrawals,
                            'isPago':r.pagado
                        }
                    )
            
            response = JsonResponse({'data': data})
            
            return response
        except Exception as e:
            return JsonResponse({'Error':e.__str__()})
    else:
        return JsonResponse({'Error':'Metodo invalidos'})


@csrf_exempt  
def ganancia_by_id(request,pk):
    
    if request.method == 'GET':
        try:
            ganancias = Registros_ganancias.objects.filter(fpa=pk)
            cpas = Registros_cpa.objects.filter(fpa=pk)
            spred = Spread.objects.all()
            data=[]
            for r in ganancias:
                if r.pagado == False and r.fecha_first_trade != None:
                    if r.partner_earning != 0:
                        monto_spread = round(calcula_porcentaje_directo(float(r.partner_earning),spred[0].porcentaje,spred[1].porcentaje),2)
                    else:
                        monto_spread = r.partner_earning
                    data.append( 
                        {
                            'creacion':r.fecha_first_trade,
                            'monto':r.partner_earning,
                            'monto_spread':monto_spread,
                            'tipo_comision':'Reverashe',
                            'client':r.client,
                            'retiro':r.withdrawals,
                            'isPago':r.pagado
                        }
                    )
            
            for c in cpas:
                data.append( 
                        {
                            'creacion':c.fecha_creacion,
                            'monto':c.monto,
                            'monto_spread':c.monto,
                            'tipo_comision':'CPA',
                            'client':c.client,
                            'retiro':0,
                            'isPago':c.pagado
                        }
                    )
                
            response = JsonResponse({'data': data})
            
            return response
        except Exception as e:
            return JsonResponse({'Error':e.__str__()})
    else:
        return JsonResponse({'Error':'Metodo invalidos'})



@csrf_exempt  
def retiros_totales(request):
    
    if request.method == 'GET':
        try:
            ganancias = Registros_ganancias.objects.all()
            
            total = 0
            data=[]
            for m in ganancias:
                retiro = formatera_retiro(m.withdrawals)
                # retiro = m.withdrawals.replace(')','').strip()
                data.append({
                    'fpa':m.fpa,
                    'fecha':m.fecha_first_trade,
                    'retiro':retiro
                })
            
            response = JsonResponse({'data':data})
            
            return response
        except Exception as e:
            return JsonResponse({'Error':e.__str__()})
    else:
        return JsonResponse({'Error':'Metodo invalidos'})

@csrf_exempt  
def ganancias_total(request):
    
    if request.method == 'GET':
        try:
            
            ganancias = Registros_ganancias.objects.all()
            
            total = 0
            
            for m in ganancias:
                if m.pagado == False:
                    total += m.partner_earning
            
            response = JsonResponse({'monto':total})
            
            return response
        except Exception:
            return JsonResponse({'Error':str(Exception)})
    else:
        return JsonResponse({'data':'El metodo es invalido'})


@csrf_exempt  
def ganancias_total_user(request,pk):
    
    if request.method == 'GET':
        try:
            
            ganancias = Registros_ganancias.objects.filter(fpa=pk)
            
            total = 0
            
            for m in ganancias:
                if m.pagado == False:
                    total += m.partner_earning
            
            response = JsonResponse({'monto':total})
            
            return response
        except Exception:
            return JsonResponse({'Error':str(Exception)})
    else:
        return JsonResponse({'data':'El metodo es invalido'})
@csrf_exempt  
def ganancias_total_con_porcentaje(request):
    
    if request.method == 'GET':
        try:
            
            ganancias = Registros_ganancias.objects.all()
            spred = Spread.objects.all()
            total = 0
            
            for m in ganancias:
                if m.pagado == False:
                    total += round(calcula_porcentaje_directo(float(m.partner_earning),spred[0].porcentaje,spred[1].porcentaje),2)
            
            response = JsonResponse({'monto':total})
            
            return response
        except Exception:
            return JsonResponse({'Error':str(Exception)})
    else:
        return JsonResponse({'data':'El metodo es invalido'})

def ganancias_cpa(request):
    if request.method == 'GET':
        try:
            
            cpas = Registros_cpa.objects.filter()
            
            data = []
            
            for r in cpas:
                data.append( 
                    {
                        'client':r.client,
                        'fpa':r.fpa
                        
                    }
                )
            
            return JsonResponse({'data':data})
        
        except Exception:
            return JsonResponse({'Error':Exception})
    else:
        return JsonResponse({'Error':'Metodo invalido'})

def ganancias_cpa_by_id(request,pk):
    if request.method == 'GET':
        try:
            
            cpas = Registros_cpa.objects.filter(fpa=pk)
            
            data = []
            
            for r in cpas:
                data.append( 
                    {
                        'client':r.client,
                        'fpa':r.fpa,
                        'monto':r.monto
                        
                    }
                )
            
            return JsonResponse({'data':data})
        
        except Exception:
            return JsonResponse({'Error':Exception})
    else:
        return JsonResponse({'Error':'Metodo invalido'})

@csrf_exempt  
def filtarGananciasCpa(request):
    
    if request.method == "GET":    
        try:
            ganancias = Registros_cpa.objects.all()
            data=[]
            for r in ganancias:
                data.append( 
                    {
                        'creacion':r.fecha_creacion,
                        'monto':r.monto,
                        'monto_spread':r.monto,
                        'tipo_comision':'CPA',
                        'id_usuario':r.client,
                        'codigo':r.fpa,
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
            ganancias = Registros_cpa.objects.filter(fpa=pk)
            data=[]
            for r in ganancias:
                
                data.append( 
                    {
                        'creacion':r.fecha_creacion,
                        'monto':r.monto,
                        'monto_spread':r.monto,
                        'tipo_comision':'CPA',
                        'id_usuario':r.client,
                        'codigo':r.fpa,
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
            
            ganancias = Registros_ganancias.objects.all()
            
            data = []
            
            for r in ganancias:
                monto_spread= round(calcula_porcentaje_directo(float(r.partner_earning,20,10)),2)
                data.append( 
                    {
                        'creacion':r.fecha_first_trade,
                        'monto':r.partner_earning,
                        'monto_spread':monto_spread,
                        'tipo_comision':'Reverash',
                        'id_usuario':r.client,
                        'codigo':r.fpa,
                        'isPago':r.pagado
                    }
                )
            
            return JsonResponse({'data':data})
        
        except Exception as e:
            return JsonResponse({'Error':e.__str__()})
    else:
        return JsonResponse({'Error':'Metodo invalido'})


def filtrar_ganancias_by_revshare_By_Id(request,pk):
    
    if request.method == 'GET':
        try:
            
            ganancias = Registros_ganancias.objects.filter(fpa=pk)
            spred = Spread.objects.all()
            data = []
            
            for r in ganancias:
                monto_spread= round(calcula_porcentaje_directo(float(r.partner_earning),spred[0].porcentaje,spred[1].porcentaje),2)
                if r.pagado == False and r.fecha_first_trade != None:
                    data.append( 
                        {
                            'creacion':r.fecha_first_trade,
                            'monto':r.partner_earning,
                            'monto_spread':monto_spread,
                            'tipo_comision':'Reverashare',
                            'id_usuario':r.client,
                            'codigo':r.fpa,
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
            ganancias = Registros_ganancias.objects.filter(Q(fecha_first_trade__gte=desde) & Q(fecha_first_trade__lte=hasta))
            spred = Spread.objects.all()
            data= []
            for r in ganancias:
                if r.partner_earning != 0:
                        monto_spread = round(calcula_porcentaje_directo(float(r.partner_earning),spred[0].porcentaje,spred[1].porcentaje),2)
                else:
                    monto_spread = r.partner_earning
                data.append( 
                
                    {
                        'creacion':r.fecha_first_trade,
                        'monto':r.partner_earning,
                        'monto_spread':monto_spread,
                        'tipo_comision':'Reverashe',
                        'client':r.client,
                        'retiro':r.withdrawals,
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
            ganancias = Registros_ganancias.objects.filter(Q(fecha_first_trade__gte=desde) & Q(fecha_first_trade__lte=hasta),fpa=pk,pagado=False)
            
            data= []
            monto_a_pagar=0
            for r in ganancias:
                # monto_a_pagar += calcula_porcentaje_directo(float(r.monto_a_pagar),spread[0].porcentaje,spread[1].porcentaje)
                monto_a_pagar += r.monto_a_pagar
                
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